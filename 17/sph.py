import random as rd
import numpy as np
from numpy.random import default_rng
import math as math
import time
import matplotlib.pyplot as plt

# Local dependencies
from heap import Heap
from cell import Cell

# Parameters
num = 1 << 10
dt = 0.01
print("Number of particles:", num)

# Init random generator
rg = np.random.default_rng()

# Initializing particles
pos = rg.random((num, 2))
vel = np.zeros((num, 2))
velPred = np.zeros((num, 2))
acc = np.zeros((num, 2))
e = np.zeros((num, 2))
e_pred = np.zeros((num, 2))
e_dot = np.zeros((num, 2))
rho = np.zeros((num))
c = np.zeros((num))
mass = np.ones((num))

def driftOne():
    global pos, velPred, e_pred
    # r += v * dt
    pos += vel * dt
    # v_pred = v + a * dt
    velPred = vel + acc * dt
    # e_pred = e + e_dot * dt
    e_pred = e + e_dot * dt

def driftTwo():
    global pos
    # r += v * dt
    pos += vel * dt

def kick():
    global vel, e
    # v += a * dt
    vel += acc * dt
    # e += e_dot * dt
    e += e_dot * dt

def monohan(r, h):
    if r == 0 or (r > 0 and r / h < 0.5):
        return (6 * (r / h) ** 3 - 6 * (r / h) ** 2 + 1)
    elif r/h >= 0.5 and r / h <= 1:
        return (2 * (1-(r / h) ) ** 3)

def dMonohan(r, h):
    if r == 0 or (r > 0 and r / h < 0.5):
        return (3 * (r / h) ** 2 - 2 * (r / h))
    elif r/h >= 0.5 and r / h <= 1:
        return ((1-(r / h) ) ** 2)
    return 0

def gradMonohan(ra, rb, h):
    rab = ra - rb
    absRab = math.sqrt(rab.dot(rab))
    dWdr = dMonohan(absRab, h)
    grad = dWdr * rab / absRab
    return grad

def calcForce():
    # Build tree
    root = Cell(0, 0, num, pos, [0,0], [1,1])   

    for a in range(num):
        heap = Heap(32)
        root.kNearest(pos[a], heap)

        # Calculate p_a
        factor = (40 / (7*math.pi)) / (heap.getMax() ** 2)
        sumMassMonohan = 0
        for i in range(heap.size):
            b = heap.indices[i]
            massCurrent = mass[b]
            h = heap.getMax()
            r = heap.values[i]
            sumMassMonohan += factor * massCurrent * monohan(r, h)

        rho[a] = sumMassMonohan

        # Caclulate c
        gamma = 2
        c[a] = math.sqrt( e[a] * gamma* (1 - gamma))
    
    # Second loop is required since all c's have to be calculated
    for a in range(num):
        # Calculate e_dot
        e_dot[a] = 0
        f_a = c[a] ** 2 / (2. * rho[a])

        for i in range(heap.size):
            b = heap.indices[i]
            f_b = c[b] ** 2 / (2. * rho[b])
            h = heap.getMax()
            r = heap.values[i]
            print(f_a, f_b)
            e_dot[a] += f_a * mass[b] * (vel[a] - vel[b]) * monohan(r, h)
            acc[a] -= mass[b] * (f_a + f_b) * monohan(r, h)

def update(time):
    driftOne()
    calcForce()
    kick()
    driftTwo()

update(10)