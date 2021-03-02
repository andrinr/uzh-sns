import random as rd
import math as math
import time
import matplotlib.pyplot as plt

# Binary tree
class Cell:

    def __init__(self, parent, dimension, left, right, particles, boundA, boundB):
        self.left = left
        self.right = right
        self.boundA = boundA
        self.boundB = boundB
        self.particles = particles
        self.parent = parent
        self.dimension = dimension
        self.isLeaf = False
        self.splitPosition = 0

        if (self.right - self.left > 64):
            self.partition()
        else:
            self.isLeaf = True
            # Determine radius
            self.radius = 0
            for particle in self.particles[self.left : self.right]:
                self.radius = max(self.radius, self.dist(self.center(), particle))

    # O(n*log(n))
    def partition(self):
        # random initial guess
        guess = (self.boundA[self.dimension] + self.boundB[self.dimension])/2
        count = self.right - self.left
        halfCount = round(count / 2)

        # binary search over float, 64bit
        # Starting at 4 because range is between 0 and 1
        # Initial guess is at 0.5, thus next guess 
        for i in range(2, 64, 1):
            nLeft = 0
            for j in range(self.left, self.right):
                # branchless counting
                nLeft += (self.particles[j][self.dimension] < guess)

            # guess improvement
            guess += ((nLeft < halfCount) - (nLeft > halfCount)) * 1/(2<<i)

            # assuming power of two total particle count, where power >= 3
            # assuming unique particle positions
            # probablity for not unqiue random float positions is ~0
            if(abs(nLeft - halfCount) == 0):
                break
        
        # single iteration of quicksort, O(n)
        i = 0
        j = count - 1
        while(i < halfCount and j >= halfCount):
            if (self.particles[self.left + i][self.dimension] > guess):
                tmp = self.particles[self.left + j]
                self.particles[self.left + j] = self.particles[self.left + i]
                self.particles[self.left + i] = tmp
                j -= 1
            else:
                i += 1

        self.splitPosition = guess

        newBoundA = self.boundA.copy()
        newBoundB = self.boundB.copy()
        newBoundA[self.dimension] = self.splitPosition
        newBoundB[self.dimension] = self.splitPosition
        self.childA = Cell(self, 1-self.dimension, self.left, self.left + halfCount, self.particles, self.boundA, newBoundB)
        self.childB = Cell(self, 1-self.dimension, self.left + halfCount, self.right, self.particles, newBoundA, self.boundB)

        center = self.center()
        centerA = self.childA.center()
        centerB = self.childB.center()
        self.radius = max(self.dist(center, centerA) + self.childA.radius, self.dist(center, centerB) + self.childB.radius)

    # Get center of cell, in this case center of square, not average of particles
    def center(self):
        return [(self.boundA[0] + self.boundB[0]) / 2, (self.boundA[1] + self.boundB[1]) / 2]

    # Find leaf where position is located within
    def findCell(self, position):
        if not self.isLeaf:
            if position[self.dimension] < self.splitPosition:
                return self.childA.findCell(position)
            else:
                return self.childB.findCell(position)
        else:
            return self

    # Distance function
    # In this case using a circle, not a box
    def dist(self, a, b):
        x = abs(a[0] - b[0])
        y = abs(a[1] - b[1])
        # Periodic boundaries
        x = min(x, 1-x)
        y = min(y, 1-y)
        return math.sqrt(x * x + y * y)

    def ballWalk(self, position, r):
        count = 0
        if (self.isLeaf):
            for particle in self.particles[self.left : self.right]:
                count += (self.dist(position, particle) < r)
        else:
            if (self.dist(position, self.childA.center()) < r + self.childA.radius):
                count += self.childA.ballWalk(position, r)

            if (self.dist(position, self.childB.center()) < r + self.childB.radius):
                count += self.childB.ballWalk(position, r)

        return count

def buildTree(num):
    particles = []
    for i in range(num):
        particles.append([rd.random(), rd.random()])

    return Cell(False, 0, 0, num, particles, [0,0], [1,1])

num = 2 << 15
root = buildTree(num)

print("Fun fact: the ballwalk algorithm can approximate PI:")
d = 0.5
print( (root.ballWalk([0.5, 0.5], d) / num) / (d/2))

print("Checking weather periodic boundaries work, should also return a number ~ 3.1 ")
# We pick a random center
# without periodic boundaries this will return a wrong value when the random center is far from 0.5 0.5
print( (root.ballWalk([rd.random(), rd.random()], d) / num) / (d/2))

# Scaling test
scales = []
times = []

for i in range(9, 18):
    num = 2 << i
    scales.append(num)
    root = buildTree(num)
    start = time.time()
    root.ballWalk([0, 0], 0.2)
    end = time.time()
    times.append(end - start)

plt.plot(scales, times)
plt.show()