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
pos = rg.random((num, 2))
vel = np.zeros((num, 2))
velPred = np.zeros((num, 2))
acc = np.zeros((num, 2))
e = np.zeros((num))
e_pred = np.zeros((num))
e_dot = np.zeros((num))
rho = np.zeros((num))
c = np.zeros((num))
mass = np.ones((num))

# Temp values, v_pred 0:1, a 2:3, e_pred 4, e_dot 5
tmps = np.zeros((num, 6))
dt = 0.01

def driftOne():
    # r += v * dt
    pos = pos + vel * dt
    # v_pred = v + a * dt
    velPred = vel + acc * dt
    # e_pred = e + e_dot * dt
    e_pred = e + e_dot * dt

def driftTwo():
    # r += v * dt
    pos = pos + vel * dt

def kick():
    # v += a * dt
    vel = vel + acc * dt
    # e += e_dot * dt
    e =  e + e_dot * dt

def monohan(r, h):
    if r > 0 and r / h < 0.5:
        return (6 * (r / h) ** 3 - 6 * (r / h) ** 2 + 1)
    elif r/h >= 0.5 and r / h <= 1:
        return (2 * (1-(r / h) ) ** 3)

def calcForce():
    # Build tree
    root = Cell(0, 0, num, pos, [0,0], [1,1])

    for a in range(num):
        heap = Heap(32)
        root.kNearest(pos[a], heap)

        # Calculate p_a
        factor = (40 / (7*math.pi)) / (heap.getMax() ** 2)
        for i in range(heap.size):
            b = heap.indices[b]
            massCurrent = mass[b]
            h = heap.getMax()
            r = heap.values[i]

            sumMassMonohan += factor * massCurrent * monohan(r, h)
            
        rho[a] = sumMassMonohan

        # Caclulate c
        gamma = 2
        c[a] = math.sqrt( e[a] * gamma* (1 - gamma))
            
        # Calculate e_dot
        factor[a] = c / (2 * rho[a])
        e_dot[a] = 0

        for i in range(heap.size):
            b = heap.indices[b]
            h = heap.getMax()
            r = heap.values[i]
            e_dot[a] += mass[b] * (vel[a] - vel[b]) * monohan(r, h)
            # Fix this: factor[b] will not be calculated before this
            acc[a] -= mass[b] * (factor[a] * factor[b]) * monohan(r, h)

def update(time):
    driftOne()
    calcForce()
    kick()
    driftTwo()

update(10)