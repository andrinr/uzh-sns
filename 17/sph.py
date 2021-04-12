import random as rd
import numpy as np
from numpy.random import default_rng
import math as math
import time
import matplotlib.pyplot as plt

# Local dependencies
from heap import Heap
from cell import Cell

class SPH:
    def __init__(self, num, dt):
        self.num = num
        self.dt = dt

        # Init random generator
        rg = np.random.default_rng()

        # Initializing particles
        self.pos = rg.random((num, 2))
        self.vel = np.zeros((num, 2))
        self.velPred = np.zeros((num, 2))
        self.acc = np.zeros((num, 2))
        self.e = np.full((num), 0.1)
        self.e_pred = np.zeros((num))
        self.e_dot = np.zeros((num))
        self.rho = np.zeros((num))
        self.c = np.zeros((num))
        self.mass = np.ones((num))

    def driftOne(self):
        # r += v * dt
        self.pos += self.vel * self.dt
        # v_pred = v + a * dt
        self.velPred = self.vel + self.acc * self.dt
        # e_pred = e + e_dot * dt
        self.e_pred = self.e + self.e_dot * self.dt

    def driftTwo(self):
        # r += v * dt
        self.pos += self.vel * self.dt

    def kick(self):
        # v += a * dt
        self.vel += self.acc * self.dt
        # e += e_dot * dt
        self.e += self.e_dot * self.dt

    def monohan(self, r, h):
        if r == 0 or (r > 0 and r / h < 0.5):
            return (6 * (r / h) ** 3 - 6 * (r / h) ** 2 + 1)
        elif r/h >= 0.5 and r / h <= 1:
            return (2 * (1-(r / h) ) ** 3)

    def dMonohan(self, r, h):
        if r == 0 or (r > 0 and r / h < 0.5):
            return (3 * (r / h) ** 2 - 2 * (r / h))
        elif r/h >= 0.5 and r / h <= 1:
            return ((1-(r / h) ) ** 2)
        return 0

    def gradMonohan(self, ra, rb, h):
        rab = ra - rb
        absRab = math.sqrt(rab.dot(rab))
        dWdr = self.dMonohan(absRab, h)
        grad = dWdr * rab / absRab
        return grad

    def calcForce(self):
        # Build tree
        root = Cell(0, 0, self.num, self.pos, [0,0], [1,1])   

        for a in range(self.num):
            heap = Heap(32)
            root.kNearest(self.pos[a], heap)

            # Calculate p_a
            factor = (40 / (7*math.pi)) / (heap.getMax() ** 2)
            sumMassMonohan = 0
            h = heap.getMax()

            for i in range(heap.size):
                b = heap.indices[i]
                massCurrent = self.mass[b]
                r = heap.values[i]
                sumMassMonohan += factor * massCurrent * self.monohan(r, h)

            self.rho[a] = sumMassMonohan

            # Caclulate c
            gamma = 2
            self.c[a] = math.sqrt( self.e[a] * gamma* (gamma - 1))
        
        # Second loop is required since all c's have to be calculated
        for a in range(self.num):
            # Calculate e_dot
            self.e_dot[a] = 0
            f_a = self.c[a] ** 2 / (2. * self.rho[a])

            h = heap.getMax()
            pos_a = self.pos[a]

            for i in range(heap.size):
                b = heap.indices[i]
                if a != b:
                    f_b = self.c[b] ** 2 / (2. * self.rho[b])
                    pos_b = self.pos[b]

                    self.e_dot[a] += f_a * self.mass[b] * (self.vel[a] - self.vel[b]).dot(self.gradMonohan(pos_a, pos_b, h))
                    self.acc[a] -= self.mass[b] * (f_a + f_b) * self.gradMonohan(pos_a, pos_b, h)

    def update(self):
        print(self.pos[0], self.vel[0], self.acc[0], self.e[0], self.e_dot[0], self.rho[0], self.mass[0], self.c[0])
        self.driftOne()
        self.calcForce()
        self.kick()
        self.driftTwo()
