# Libraries
import numpy as np
import matplotlib.pyplot as plt
# Local Dependencies
from Eliptic import Eliptic
from Electrons import Electrons
from grid_interpolations import bicubic
from solvers import ode_solver
from solvers import runge_kutta_fourth_step

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

# Line plots
ax_main = fig.add_subplot(gs[:, :])

# Calculate potential field
N = 100
ax_main.set_ylim(0, N)
ax_main.set_xlim(0, N)
omega = 2 / ( 1 + np.pi / N)
boundary = np.full((N,N), omega)

boundary[0, :] = 0
boundary[-1, :] = 0
boundary[:, 0] = 0
boundary[:, -1] = 0
boundary[int(0.5*N), int(0.25*N):int(0.75*N)] = 0

# init potential grid
P = np.zeros((N, N))

# Add wire with 1000V potential
P[int(0.5*N), int(0.25*N):int(0.75*N)] = -1000

eliptic = Eliptic(N, P, boundary)
eliptic.solve(0.01)
eliptic.plot(ax_main)

# Electrons
electrons = Electrons(100, P, ode_solver, runge_kutta_fourth_step, bicubic)
electrons.solve(500, 10**-16)
electrons.plot(ax_main, N)

plt.show()