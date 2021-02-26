import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import math as math

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:

    def __init__(self, left, right, particles, boundA, boundB):
        self.left = left
        self.right = right
        self.boundA = boundA
        self.boundB = boundB
        self.particles = particles

    def partition(self, dimension):
        guessX = (self.boundA.x + self.boundB.x)/2
        guessY = (self.boundA.y + self.boundB.y)/2
        halfCount = round((self.right - self.left) / 2)

        for i in range(4, int(math.log2(self.right - self.left))**2, 1):
            count = 0
            for j in range(self.left, self.right):
                # Not sure if branchless option indeed gives a speedup
                count += (self.particles[j].x < guessX) * dimension 
                count += (self.particles[j].y < guessY) * (1-dimension)

            # branchless narrowing down guess
            guessX += ((count < halfCount) - (count > halfCount)) * 1/i * dimension
            guessY += ((count < halfCount) - (count > halfCount)) * 1/i * (1-dimension)

            if(abs(count - halfCount) < 1):
                print(count)
                break

        for j in range(self.left, self.right):


        



particles = []
num = 2 << 12
print("total", num)
for i in range(num):
    particles.append(Point(rd.random(), rd.random()))


root = Cell(0, num, particles, Point(0,0), Point(1,1))

root.partition(0)