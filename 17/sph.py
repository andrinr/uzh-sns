import random as rd
import numpy as np
from numpy.random import default_rng
import math as math
import time
import matplotlib.pyplot as plt

# Local dependencies
from heap import Heap
from cell import Cell

num = 1 << 10
print("Number of particles:", num)

# Init random generator
rg = np.random.default_rng()

# Initializing particles
# Particle array: rx, ry, vx, vy, e, c, p, h
# = 8 Dimensions
particles = np.zeros((num, 8))
# Random positions
positions = rg.random((num,2))

particles[:,0:2] = rg.random((num,2))
# Constant energy
particles[:,4] = rg.ones((num,2))
# Constant density
particles[:,6] = rg.ones((num,2))

# Temp values, v_pred, a, e_pred, e_dot
tmps = np.zeros((num, 6))

root = Cell(0, 0, num, particles[:,0:3], [0,0], [1,1])
fig, axes = plt.subplots(1,2)

dt = 0.01

def driftOne():
    # r += v * dt
    particles[:,0:2] += particles[:,2:4] * dt
    # v_pred = v + a * dt
    tmps[:,0,2] = particles[:,0:2] + dt * tmps[:,2:4]
    # e_pred = e + e_dot * dt
    tmps[:, 4] = particles[:, 5] + dt * tmps[:,5]

def driftTwo():
    # r += v * dt
    particles[:,0:2] += particles[:,2:4] * dt

def kick():
    # v += a * dt
    particles[:,2:4] += tmps[:,2:4] * dt
    # e += e_dot * dt
    particles[:,4] += tmps[:,5] * dt

def calcForce():
    # Build tree
    root = Cell(0, 0, num, particles, [0,0], [1,1])
    # All particles calculate p_a

    # All particles caclulate c

    # All particles calcaulte a, e_dot

driftOne()
calcForce()

def update(time):
    driftOne()
    calcForce()
    kick()
    driftTwo()


for particle in particles:
    maxHeap = Heap(32)
    root.kNearest(particle[0:2], maxHeap)

    # Monohan factor
    factor = (40 / (7*math.pi)) / (maxHeap.getMax() ** 2)

    sumMass = 0
    sumMassMonohan = 0
    for i in range(maxHeap.size):
        mass = maxHeap.data[i][2]
        sumMass += mass
        h = maxHeap.getMax()
        r = maxHeap.values[i]
        if r > 0 and r / h < 0.5:
            sumMassMonohan += mass * (6 * (r / h) ** 3 - 6 * (r / h) ** 2 + 1)
        elif r/h >= 0.5 and r / h <= 1:
            sumMassMonohan += mass * (2 * (1-(r / h) ) ** 3)
        
    
    # Top hat
    particle[3] = sumMass / ( math.pi * maxHeap.getMax() ** 2)
    
    particle[4] = sumMassMonohan

axes[1].set_title("Top hat density of 32 nearest")
scatter = axes[1].scatter(particles[:,0], particles[:,1], c = particles[:,3])
scatter = axes[0].scatter(particles[:,0], particles[:,1], c = particles[:,4])
fig.colorbar(scatter, ax = axes[1])
plt.show()

