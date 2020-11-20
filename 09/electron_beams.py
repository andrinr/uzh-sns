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
from matplotlib.animation import FuncAnimation

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 2)

# Line plots
ax_main = fig.add_subplot(gs[:, :-1])
ax_top_right = fig.add_subplot(gs[0, -1])
ax_bottom_right = fig.add_subplot(gs[1, -1])

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

# init potential grid
P = np.zeros((N, N))


# Design number one
#count  = 150
#x = np.linspace(0,0.999, count)
#line_x = np.floor(x*N).astype(int)
#line1_y = np.floor((-(0.9 - 0.4)*x + 0.95)*N).astype(int)
#line2_y = np.floor((-(0.9 - 0.4)*x + 0.55)*N).astype(int)
#line3_y = np.floor((-(0.9 - 0.4)*x + 0.75)*N).astype(int)
#print(line1_y)
#boundary[line_x, line1_y-1] = 0
#P[line_x, line1_y-1] = -100
#boundary[line_x, line2_y+1] = 0
#P[line_x, line2_y+1] = -100
#
#boundary[line_x, line1_y] = 0
#P[line_x, line1_y] = -1000
#boundary[line_x, line2_y] = 0
#P[line_x, line2_y] = -1000
#
#boundary[line_x, line3_y] = 0
#for i in range(count):
#    P[line_x[i], line3_y[i]] = (i/count)**2*1000

# Design number two

# Mirror 1
#mirror_strength = -400
#y = int(0.55*N)
#
#boundary[0:int(N/8), y] = 0
#P[ 0:int(N/2), y] = mirror_strength
##boundary[0:int(N/4), y+1] = 0
##P[ 0:int(N/2), y+1] = 0
#
## Mirror 2
#y = int(0.95*N)
#boundary[0:int(N/8), y] = 0
#P[ 0:int(N/2), y] = mirror_strength
##boundary[0:int(N/4), y+1] = 0
##P[ 0:int(N/2), y+1] = mirror_strength
#
## Accelerator 1
##y = int(0.75*N)
##boundary[int(N/5):int(N/5*2), y] = 0
##P[ int(N/4):int(N/4*2), y] = 1000
#
#count  = 100
#x = np.linspace(0,0.999, count)
#line_x = np.floor(x*N).astype(int)
#line3_y = np.floor((-(0.9 - 0.4)*x + 0.75)*N).astype(int)
#
#for i in range(count):
#    boundary[line_x[i], line3_y[i]] = 0
#    P[line_x[i], line3_y[i]] = 200 + 800/count*i

# Accelerator 2
#y = int(0.95*N)
#boundary[int(N/4):int(N/4*2), y] = 0
#P[int(N/4):int(N/4*2), y] = 1000


#boundary[int(0.55*N), 0:int(N/4)] = 0
#P[int(0.55*N), 0:int(N/2)] = -1000
#
#boundary[int(0.55*N), 0:int(N/4)] = 0
#P[int(0.55*N), 0:int(N/2)] = -400
#
#boundary[int(0.95*N), 0:int(N/4)] = 0
#P[int(0.95*N), 0:int(N/2)] = -400
#
#boundary[int(0.55*N), int(N/4*2):int(N/4)] = 0
#P[int(0.55*N),  int(N/4*2):int(N/4)] = 1000
#
#boundary[int(0.95*N),  int(N/4*2):int(N/4)] = 0
#P[int(0.95*N), int(N/4*2):int(N/4)] = 1000

# Design 3

#y = int(0.75*N)
#x = int(0.1*N)
#boundary[x, y] = 0
#P[x, y] = 1000
#
#y = int(0.95*N)
#x = int(0.05*N)
#boundary[0:x, y] = 0
#P[0:x, y] = -500
#
#y = int(0.55*N)
#x = int(0.05*N)
#boundary[0:x, y] = 0
#P[0:x, y] = -500


# Design 4

center_x = int(0.1*N)
start_y = int(0.99 * N)
slope = 1
length = 0.2*N
x = (np.linspace(0, 1, int(length))*length).astype(int)

print(x)

#y_1 = (start_y + slope * x).astype(int)
y_2 = (start_y - slope * x).astype(int)

#print(y_1)
print(y_2)
#boundary[x+center_x, y_1] = 0
#P[x+center_x, y_1] = 1000
boundary[x+center_x, y_2] = 0
P[x+center_x, y_2] = 1000

#boundary[x+center_x+1, y_1] = 0
#P[x+center_x+1, y_1] = 0
boundary[x+center_x+1, y_2] = 0
P[x+center_x+1, y_2] = 0


eliptic = Eliptic(N, P, boundary)
eliptic.solve(10**-28, 10**3)
eliptic.plot(ax_main)

frames = 1000

# Electrons
# Using bilinear over bicubic interpolation for greatly improved runtime, around 10x faster
electrons = Electrons(100, P, [0.01, 0.01], runge_kutta_fourth_step, bilinear, 10**-10*0.5, frames)
#electrons.solve(1000, 10**-10*0.5)
#electrons.plot(ax_main, ax_top_right, ax_bottom_right, N)

electrons.init_plot(ax_main, ax_top_right, N)

ani = FuncAnimation(fig, electrons.step, frames=range(frames), interval=1, repeat=False)


plt.show()