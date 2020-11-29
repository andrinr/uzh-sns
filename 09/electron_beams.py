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
gs = fig.add_gridspec(3, 2)

# Line plots
ax_main = fig.add_subplot(gs[:, :-1])
ax_top_right = fig.add_subplot(gs[:, -1])

# Calculate potential field
N = 150
ax_main.set_ylim(0, N)
ax_main.set_xlim(0, N)
omega = 2 / (1 + np.pi / N)
boundary = np.full((N, N), omega)

#boundary[0, :] = 0
#boundary[-1, :] = 0
#boundary[:, 0] = 0
#boundary[:, -1] = 0

# init potential grid
P = np.zeros((N, N))


x = (np.linspace(-0.499, 0.499, 200)*N).astype(int)
y = -0.34*x + 0.5*N
y = y.astype(int)
x = 0.5*N + x
x = x.astype(int)

boundary[x, y] = 0
P[x, y] = 1000


eliptic = Eliptic(N, P, boundary)
eliptic.solve(10**-28, 10**3)
eliptic.plot(ax_main)

# Electrons
# Using bilinear over bicubic interpolation for greatly improved runtime, around 10x faster
electrons = Electrons(150, P, [0.01, 0.01], runge_kutta_fourth_step, bilinear)
electrons.solve(1000, 10**-10*0.5)
electrons.plot(ax_main, ax_top_right, N)

plt.show()