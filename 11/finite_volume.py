import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Define constants
delta_x = 0.01
delta_y = 0.01

vel_x = 10
vel_y = 10

# Calculate delta t such that c_x + c_y = 1
# add factor 0.5 for improved prevision => c_x + c_y = 0.5 < 1
delta_t =  1 / (vel_x / delta_x + vel_y / delta_y)

c_x = vel_x * delta_t / delta_x
c_y = vel_y * delta_t / delta_y

print(c_x, c_y, c_x + c_y)

# CIR positive positive kernel
kernel_cir_pp = np.array([
    [0,     0,              0],
    [c_x,   1 - c_x - c_y,  0],
    [0,     c_y,            0]
])

# CTU positive positive kernel
kernel_ctu_pp = np.array([
    [0,              0,                     0],
    [c_x*(1-c_y),   (1 - c_x) * (1-c_y),    0],
    [c_x*c_y,       (1-c_x)*c_y,            0]
])

print(kernel_cir_pp)
print(kernel_ctu_pp)

def cir_step(grid):
    if vel_x > 0 < vel_y:
        return ndimage.convolve(
            grid, kernel_cir_pp.T, mode="wrap"
        )


def ctu_step(grid):
    if vel_x > 0 < vel_y:
        return ndimage.convolve(
            grid, kernel_ctu_pp.T, mode="wrap"
        )

# initialize grids
N = 150
grid_init = np.zeros((N, N))

grid_1 = np.zeros((N, N))
grid_2 = np.zeros((N, N))

sigma_x = 0.02
sigma_y = sigma_x
for i in range(N):
    for j in range(N):
        x = (N/2 - i) / N
        y = (N/2 - j) / N
        grid_init[i][j] = np.exp(-x**2 / (2*sigma_x*sigma_x) - y**2 / (2*sigma_y*sigma_y))

grid_1 = grid_init
grid_2 = grid_1

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

## Line plots
ax_tl = fig.add_subplot(gs[0, 0])
ax_ml = fig.add_subplot(gs[1, 0])

ax_tm = fig.add_subplot(gs[0, 1])
ax_tm.set_title("X Axis cross section for each CIR cycle")
ax_mm = fig.add_subplot(gs[1, 1])
ax_mm.set_title("X Axis cross section for each CTU cycle")
ax_tr = fig.add_subplot(gs[0, 2])
ax_tr.set_title("Y Axis cross section for each CIR cycle")
ax_mr = fig.add_subplot(gs[1, 2])
ax_mr.set_title("Y Axis cross section for each CTU cycle")

cycles = 15
iterations_per_cycle = 100
iterations = cycles * iterations_per_cycle

j = 0
for i in range(iterations):
    grid_1 = cir_step(grid_1)
    grid_2 = ctu_step(grid_2)

    if i % iterations_per_cycle == 0:

        ax_tm.plot(grid_1[int(N/2), :])
        ax_mm.plot(grid_2[int(N/2), :])

        ax_tr.plot(grid_1[:, int(N/2)])
        ax_mr.plot(grid_2[:, int(N/2)])

        j += 1


ax_tl.set_title("Mass after 15 cycles with CIR")
im1 = ax_tl.imshow( grid_1)
fig.colorbar(im1, ax=ax_tl)

ax_ml.set_title("Mass after 15 cycles with CTU")
im2 = ax_ml.imshow(grid_2)
fig.colorbar(im2, ax=ax_ml)

plt.show()