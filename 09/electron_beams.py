# Libraries
import numpy as np
import matplotlib.pyplot as plt
# Local Dependencies
from Eliptic import Eliptic
from Particle import Particle
from grid_interpolations import bilinear

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2, 3)

# Line plots
ax_main = fig.add_subplot(gs[1,:])

# Calculate potential field
N = 20
omega = 2 / ( 1 + np.pi / N)
boundary = np.full((N,N), omega)

boundary[0,:] = 0
boundary[-1,:] = 0
boundary[:,0] = 0
boundary[:,-1] = 0
boundary[int(0.5*N),int(0.25*N):int(0.75*N)] = 0

# init potential grid
P = np.ones((N, N))

# Add wire with 1000V potential
P[int(0.5*N),int(0.25*N):int(0.75*N)] = 1000

eliptic = Eliptic(N, P, boundary)
eliptic.solve(0.01)
eliptic.plot(ax_main)

# Test bilinear interpolation
N2 = 100
ip = np.zeros((N2,N2))

ax_top = fig.add_subplot(gs[0,:])

for i in range(N2):
    for j in range(N2):
        ip[i,j] = bilinear(P,[1/N2*i,1/N2*j])

ax_top.imshow(ip,cmap="plasma")

particles = []
for i in range(1000):
    particles.append(Particle(0,0))


plt.show()