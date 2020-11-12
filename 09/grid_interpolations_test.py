from grid_interpolations import bicubic
from grid_interpolations import bilinear
import numpy as np
import matplotlib.pyplot as plt

# Visual test of bicubic and bilinear interpolation implementations

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# Line plots
raw_ax = fig.add_subplot(gs[:,0])
linear_ax = fig.add_subplot(gs[:,1])
cubic_ax = fig.add_subplot(gs[:,2])

N1 = 10
N2 = 100

noise = np.random.rand(N1,N1)

linear = np.zeros((N2,N2))

cubic = np.zeros((N2,N2))

for i in range(N2):
    for j in range(N2):
        linear[i,j] = bilinear(noise,[1/N2*i,1/N2*j])

for i in range(N2):
    for j in range(N2):
        cubic[i,j] = bicubic(noise,[1/N2*i,1/N2*j])

# QUESTION:
# The bicubic interpolation yields results, of which some are greater than 1 or less than 0.
# Is this expected behaviour? If not what did I do wrong?

raw_ax.imshow(noise,cmap="Greys")
linear_ax.imshow(linear,cmap="Greys")
cubic_ax.imshow(cubic,cmap="Greys")

plt.show()