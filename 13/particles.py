import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import math as math

class Cell:

    def __init__(self, left, right, particles, boundA, boundB):
        self.left = left
        self.right = right
        self.boundA = boundA
        self.boundB = boundB
        self.particles = particles

    def partition(self, dimension):
        # random initial guess
        guess = (self.boundA[dimension] + self.boundB[dimension])/2
        count = self.right - self.left
        halfCount = round(count / 2)

        # binary search over float, 64bit
        for i in range(4, 64, 1):
            count = 0
            for j in range(self.left, self.right):
                # branchless counting
                count += (self.particles[j][dimension] < guess)

            # guess improvement
            guess += ((count < halfCount) - (count > halfCount)) * 1/i

            print(count, " ", guess)
            # assuming power of two total particle count
            # assuming unique particle positions
            # probablity for not unqiue random float positions is ~0
            if(abs(count - halfCount) == 0):
                print(count)
                break

        while(j < halfCount):
            if (particles[j][dimension] > guess):
                tmp = particles[count-j-1]
                particles[count-j-1] = particles[j]
                particles[j] = tmp



        



particles = []
num = 2 << 12
print("total", num)
for i in range(num):
    particles.append([rd.random(), rd.random()])


root = Cell(0, num, particles, [0,0], [1,1])

root.partition(0)