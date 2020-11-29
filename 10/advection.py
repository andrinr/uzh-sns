import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from matplotlib.animation import FuncAnimation

class Advection:

    def __init__(self, rho_init, step_solver, u):
        self.N = len(rho_init)
        self.rho = rho_init
        self.step_solver = step_solver
        self.u = u
        self.dx = 1 / N
        self.h = self.dx / np.abs(u) * 0.5
        self.c = self.u * self.h / self.dx

    def step(self):
        if self.step_solver == 1:
            self.laax_step()
        elif self.step_solver == 2:
            self.upwind_step()
        else:
            self.lax_wendroff_step()

    def laax_step(self):
        # For the bonus points:
        # Comment/Uncomment to test

        # Var 1
        #rho_next = np.zeros(self.N)
        #for i in range(self.N):
        #    rho_next[i] = self.rho[(i-1) % self.N]*0.5*(1+self.c) + self.rho[(i+1) % self.N]*0.5*(1-self.c)

        #self.rho = rho_next

        # Var 2
        left = np.roll(self.rho, 1)
        right = np.roll(self.rho, -1)
        self.rho = left*0.5*(1+self.c) + right*0.5*(1-self.c)

        # Var 3
        #self.rho = ndimage.convolve(self.rho, [0.5*(1-self.c), 0, 0.5*(1+self.c)], mode="wrap")
        return

    def upwind_step(self):
        if self.u > 0:
            self.rho = ndimage.convolve(self.rho, np.array([0, 1-self.c, self.c]), mode="wrap")
        else:
            self.rho = ndimage.convolve(self.rho, np.array([-self.c, 1 + self.c, 0]), mode="wrap")
        return

    def lax_wendroff_step(self):
        self.rho = ndimage.convolve(self.rho,
                                    np.array([-0.5*self.c*(1-self.c), 1 - self.c**2, 0.5*self.c*(1+self.c)]),
                                    mode="wrap")
        return


fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 1)
# Line plots
ax_top = fig.add_subplot(gs[:])
ax_top.set_ylim(-0.3, 1.3)

#ax_mid = fig.add_subplot(gs[1])
#ax_mid.set_ylim(-0.3, 1.3)
#ax_bot = fig.add_subplot(gs[2])
#ax_bot.set_ylim(-0.3, 1.3)

N = 1000
rho = np.zeros(N)
rho[int(N/4): int(2*N/4)] = 1

# Something has to be wrong with the formulas, therefore I use negative velocities here
advections = [Advection(rho, 1, 1), Advection(rho, 2, 1), Advection(rho, 3, 1)]

x = np.linspace(0, 1, N)

lineplots = [
    ax_top.plot(x, advections[0].rho)[0],
    ax_top.plot(x, advections[1].rho)[0],
    ax_top.plot(x, advections[2].rho)[0]]

def update(i):
    for i in range(5):
        advections[0].step()
        advections[1].step()
        advections[2].step()

    lineplots[0].set_data(x, advections[0].rho)
    lineplots[1].set_data(x, advections[1].rho)
    lineplots[2].set_data(x, advections[2].rho)

ani = FuncAnimation(fig, update, 1000, interval=60, repeat=False)

plt.show()