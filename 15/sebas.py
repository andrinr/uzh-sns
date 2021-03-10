import numpy as np
import matplotlib.pyplot as plt
from heapq import *


#class for particles 
class particle:
    #initiates a particle at position r
    def __init__(self, r):
        self.r = r
    #calculates the distance of the particle to a location r
    def dist2(self, r):
        return(np.sum((r-self.r)**2))

    
#class for cells
class cell:
    def __init__(self, rLow, rHigh, iLower, iUpper):
        #lower and upper bounds of the cell
        self.rLow = rLow
        self.rHigh = rHigh
        #lower and upper index that corresponds to the collection of particles in the particle array
        #that belong to the cell
        self.iLower = iLower
        self.iUpper = iUpper
        #pointers to the child cells, one is described as lower, one as upper (could also use left and right), root
        #cell starts with no children per default
        self.pLower = None
        self.pUpper = None
        
    #ball_box_dist2
    #calculates the distance of a particle p to the cell, according to the described method 1 in the lecture
    def dist2(self, p):
        d2 = 0
        #center location of cell
        c = (self.rHigh + self.rLow)/2
        #vector from center to upper right corner of cell
        b = (self.rHigh - self.rLow)/2
        for dim in range(2):
            t = np.abs(c[dim] - p[dim]) - b[dim]
            if (t > 0):
                d2 += t*t
            
        return(d2)
    
#partition function, partitions an array from index i to j so that below l, only values smaller than v are found
#and above l, only values larger than v are found (partition along dimension d)
def partition(array, i, j, v, d):
    
    l = i
    
    for k in range(i,j+1):
        if array[k].r[d] < v:
            array[k], array[l] = array[l], array[k]
            l += 1
    return(l)

#builds a tree starting from a root cell and an array, given some first dimension of splitting
def treebuild(array, root, dim):
    
    #split the cell in half
    v = 0.5 * (root.rLow[dim] + root.rHigh[dim])
    #partition the array accordingly
    s = partition(array, root.iLower, root.iUpper, v, dim)

    # may have two parts: lower...s-1 and s...upper
    if s > root.iLower:
        #if a lower cell exists, create it
        rLow = np.copy(root.rLow)
        rHigh = np.copy(root.rHigh)
        rHigh[dim] = v
        cLower = cell(rLow, rHigh, root.iLower, s-1)
        #assign the created cell to be the lower child of the root
        root.pLower = cLower
        #if there are more than the threshold value of particles in the cell, split the cell further
        if len(array[root.iLower:s]) > thresh:
            treebuild(array, cLower, 1-dim)
            
    if s <= root.iUpper:
        #if an upper cell exists, create it
        rLow = np.copy(root.rLow)
        rLow[dim] = v
        rHigh = np.copy(root.rHigh)
        cUpper = cell(rLow, rHigh, s, root.iUpper)
        #assign the created cell to be the upper child of the root
        root.pUpper = cUpper
        #if there are more than the threshold value of particles in the cell, split the cell further
        if len(array[s:root.iUpper+1]) > thresh:
            treebuild(array, cUpper, 1-dim)
                  
        
#plots the tree  with the particles      
def plottree(array, root, ax, c):
    #plot all the particles
    for i in range(len(array)):
        ax.plot(array[i].r[0], array[i].r[1], "bo", markersize = 1, c = c)
    #plot the leaf cells of the tree
    drawcells(root, ax)
    ax.set_aspect("equal")

#plots the leaf cells
def drawcells(root, ax):
    #if cell has pLower, it is not a leaf. Look at the pLower cell and check if it is leaf
    if root.pLower is not None:
        drawcells(root.pLower, ax)
    #if cell has pUpper, it is not a leaf. Look at the pUpper cell and check if it is leaf
    if root.pUpper is not None:
        drawcells(root.pUpper, ax)
    #if cell has neither pLower, nor pUpper it is a leaf. plot the leaf cell as a rectangle in the given ax.
    if root.pLower is None and root.pUpper is None:
        ax.plot([root.rLow[0],root.rHigh[0],root.rHigh[0],root.rLow[0],root.rLow[0]], [root.rLow[1],root.rLow[1],root.rHigh[1],root.rHigh[1],root.rLow[1]], alpha = 0.5)
        
#counts the particles in array near r within a radius² of r2max, given some tree structure whose root is "cell"
def ball_walk_old(r, cell, r2max, array):
    #initiate counter
    count = 0
    #if the cell is a leaf, we calculate the distance to each particle in the cell, if distance is < r2max we add to count
    if cell.pUpper is None and cell.pLower is None:
        for particle in array[cell.iLower:cell.iUpper+1]:
            if particle.dist2(r.r) < r2max:
                count += 1
    else:
        #if the cell is not a leaf (e.g. the root we start from)
        #it can have either a lower or upper cell (or both), we calculate
        #the distance to those cells and consider them only if
        #they are withing r2max, thus saving computing time
        if cell.pLower is not None:
            if cell.pLower.dist2(r.r) < r2max:
                count += ball_walk_old(r, cell.pLower, r2max, array)
        if cell.pUpper is not None:
            if cell.pUpper.dist2(r.r) < r2max:
                count += ball_walk_old(r, cell.pUpper, r2max, array)
    return count


#initiate particle data: N particles in an array of dtype particle
N = 1000
particles = np.zeros(N, dtype = particle)
#populate particle array with particles at randomly distributed locations (uniform distribution)
for i in range(N):
    particles[i] = particle(np.random.random(2))
    
#initiate root cell with lower and upper bound, lower and upper index
rLow = np.array([0.,0.])
rHigh = np.array([1.,1.])

iLower = 0
iUpper = N - 1

root = cell(rLow, rHigh, iLower, iUpper)

#specify dimension in which we first split up the cell, can be either 0 (x) or 1(y)
dim = 1
#specify threshold value of maximum number of particles we want in each leaf cell
thresh = 8
#build the tree
treebuild(particles, root, dim)

#specify the radius we want to count the number of neighbours in
rmax = 0.1
r2max = rmax**2
#particle we want to count the neighbours for
test_particle = particles[int(N/2)]

#initiate plot
fig, ax = plt.subplots(1,1, figsize = (14,14))
#plot the particles and the cells
plottree(particles, root, ax, "blue")
#plot the circle surrounding our test particle, within which we look for neighbours
circle = plt.Circle((test_particle.r[0], test_particle.r[1]), radius = rmax, alpha = 0.2)
ax.add_patch(circle)
plt.show()

#perform ball walk number of neighbour counting
print("Number of neighbours: " + str(ball_walk_old(test_particle, root, r2max, particles)) + "\n")
