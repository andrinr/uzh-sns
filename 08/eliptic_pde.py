import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 200
P = np.zeros((N, N))
R = np.zeros((N, N))

kernel = np.array([[0,1,0],
                   [1,-4,1],
                   [0,1,0]])

omega = 2 / ( 1 + np.pi / N)
print(omega)

# Checkerboard pattern
checkerboard = np.full((N,N), False)
checkerboard[::2,::2] = True
checkerboard[1::2,1::2] = True

# Boundary conditions
boundary = np.full((N,N), omega)
boundary[0,:] = 0
boundary[-1,:] = 0
boundary[:,0] = 0
boundary[:,-1] = 0
boundary[int(0.5*N),int(0.25*N):int(0.75*N)] = 0

# Add shape to boundary conditions and potential data
error = []
time = []

def init():
    P[:,:] = 1
    P[int(0.5*N),int(0.25*N):int(0.75*N)] = 1000

init()

fig, axes = plt.subplots(2,1)

imgPlot = axes[0].imshow(P, cmap="plasma")

linePlot, = axes[1].plot(time, error)

frames = 200
axes[1].set_xlim(0,frames)
axes[1].set_ylim(0,10)

def update(frame):
    change_checkerboard = 0.25 * np.multiply(ndimage.convolve(P, kernel, mode='constant'), boundary)[checkerboard]
    P[checkerboard] += change_checkerboard
    change_i_checkerboard = 0.25 * np.multiply(ndimage.convolve(P, kernel, mode='constant'), boundary)[~checkerboard]
    P[~checkerboard] += change_i_checkerboard
    imgPlot.set_array(P)

    current_error = max(np.max(change_checkerboard), np.max(change_i_checkerboard))
    error.append(np.log(current_error))
    time.append(frame)

    linePlot.set_data(time, error)

    return [imgPlot, linePlot]

ani = FuncAnimation(fig, update,frames=range(frames), interval=20, repeat=False)

plt.show()