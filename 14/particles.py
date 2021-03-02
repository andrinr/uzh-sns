import random as rd
import math as math

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

        if (self.right - self.left > 8):
            self.partition()
        else:
            self.isLeaf = True

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


    # Find leaf where position is located within
    def findCell(self, position):
        if not self.isLeaf:
            if position[self.dimension] < self.splitPosition:
                return self.childA.findCell(position)
            else:
                return self.childB.findCell(position)
        else:
            return self

    #def ballWalk():



particles = []
num = 2 << 15
print("Total number of particles: ", num)
for i in range(num):
    particles.append([rd.random(), rd.random()])

# Init and build tree
print("Building tree...")
root = Cell(False, 0, 0, num, particles, [0,0], [1,1])
print("Tree built!")

randomParticle = particles[rd.randint(0,num)]
print(randomParticle)
print("Searching for kNearest particles using binary tree. Nearest particles to: ", randomParticle)
k = 8
cell = root.findCell(randomParticle)
print(cell.boundA, cell.boundB)

