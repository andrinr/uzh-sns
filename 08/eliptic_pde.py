import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Elyptic:
    
    def __init__(self, N, omega, kernel):
        self.N = N
        self.omega = omega
        self.kernel = kernel

        self.reset()
    
    def reset(self):
        # reset time and error
        self.error = []
        self.time = []

         # Create checkerboard boolean Map
        self.checkerboard = np.full((N,N),False)
        self.checkerboard[::2,::2] = True
        self.checkerboard[1::2,1::2] = True

        # init potential grid
        self.P = np.ones((self.N,self.N))

        # Add wire with 1000V potential
        self.P[int(0.5*N),int(0.25*N):int(0.75*N)] = 1000

        # init boundary conidtions
        self.boundary = np.full((self.N,self.N), self.omega)
        self.boundary[0,:] = 0
        self.boundary[-1,:] = 0
        self.boundary[:,0] = 0
        self.boundary[:,-1] = 0
        # Add boundary conditions to wire to leave it unaffected
        self.boundary[int(0.5*self.N),int(0.25*self.N):int(0.75*self.N)] = 0

    # Solver step
    def step(self, iteration):
        # Apply kernel, multiply by boundary and checkerboard
        change_checkerboard = 0.25 * np.multiply(ndimage.convolve(self.P, self.kernel, mode='constant'), self.boundary)[self.checkerboard]
        self.P[self.checkerboard] += change_checkerboard
    
        # Apply kernel, multiply by boundary and inverse checkerboard
        change_i_checkerboard = 0.25 * np.multiply(ndimage.convolve(self.P, self.kernel, mode='constant'), self.boundary)[~self.checkerboard]
        self.P[~self.checkerboard] += change_i_checkerboard

        # Get maximum error over domain
        current_error = max(np.max(change_checkerboard), np.max(change_i_checkerboard))

        # Store error and time
        self.error.append(np.log(current_error))
        self.time.append(iteration)

        return self.P, self.error, self.time


# Plotting
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

# Line plots
ax_bottom = fig.add_subplot(gs[1,:])
frames = 250
ax_bottom.set_xlim(0,frames)
ax_bottom.set_ylim(-8,8)

linePlots = []
linePlots.append(ax_bottom.plot([], [])[0])
linePlots.append(ax_bottom.plot([], [])[0])
linePlots.append(ax_bottom.plot([], [])[0])
ax_bottom.set_title("log plots of max error over time")
plt.legend(["omega = 1", "omega = 2 / (1 + pi / N)", "omega 2"], loc=1)
# IMG plots
axes = []

axes.append(fig.add_subplot(gs[0,0]))
axes[0].set_title("omega = 1, slow")
axes.append(fig.add_subplot(gs[0,1]))
axes[1].set_title("omega = 2 / (1 + pi / N), fast, stable")
axes.append(fig.add_subplot(gs[0,2]))
axes[2].set_title("omega = 2, fast, unstable")

imgPlots = []

# Calculations
potentials = []
N = 100
count = 3
kernel = np.array([[0,1,0],
                   [1,-4,1],
                   [0,1,0]])


# Init animation
def init():
    # slow, stable and unstable behaviour
    omegas = [1, 2 / ( 1 + np.pi / N), 2]

    for i in range(count):
        potentials.append(Elyptic(N,omegas[i],kernel))
        imgPlots.append(axes[i].imshow(potentials[i].P, cmap="plasma"))


# Update animation
def update(frame):

    for i in range(count):
        P, error, time = potentials[i].step(frame)
        imgPlots[i].set_array(P)
        linePlots[i].set_data(time,error)

    return [imgPlots, linePlots]

ani = FuncAnimation(fig, update,init_func=init,frames=range(frames), interval=20, repeat=False)

# Make fullscreen to have good layout
plt.show()