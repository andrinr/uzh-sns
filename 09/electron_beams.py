# Libraries
import numpy as np
import matplotlib.pyplot as plt
# Local Dependencies
from Eliptic import Eliptic
from Electrons import Electrons
from grid_interpolations import bilinear
from grid_interpolations import bicubic
from solvers import ode_solver
from solvers import runge_kutta_fourth_step
from solvers import leap_frog_step

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

# Line plots
ax_main = fig.add_subplot(gs[:, :])

# Calculate potential field
N = 100
ax_main.set_ylim(0, N)
ax_main.set_xlim(0, N)
omega = 2 / (1 + np.pi / N)
boundary = np.full((N, N), omega)

boundary[0, :] = 0
boundary[-1, :] = 0
boundary[:, 0] = 0
boundary[:, -1] = 0
boundary[int(0.5*N), int(0.25*N):int(0.75*N)] = 0

# init potential grid
P = np.zeros((N, N))

# Add wire with 1000V potential
P[int(0.5*N), int(0.25*N):int(0.75*N)] = 100

eliptic = Eliptic(N, P, boundary)
eliptic.solve(0.01)
eliptic.plot(ax_main)

# Electrons
# Using bilinear over bicubic interpolation for greatly improved runtime, around 10x faster
electrons = Electrons(1, P, [0.01, 0.01], runge_kutta_fourth_step, bilinear)
electrons.solve(500, 10**-9)
electrons.plot(ax_main, N)

plt.show()