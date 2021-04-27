import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class tour:

    def __init__(self, N):
        self.rg = np.random.default_rng()
        self.nodes = self.rg.random((N, 2))
        self.path = np.arange(N)
        self.N = N

        # Calculate initial T
        maxE = 0
        for i in range(100):
            e, p = self.trySwap()  
            maxE = max(e,maxE)

        self.T = maxE

        # Pick minimum energy from 1000 random paths
        minE = self.N * 100
        minP = self.path
        for i in range(1000):
            e, p = self.tryPath()
            if (e < minE):
                minE = e
                minP = p

        self.path = minP

    def tryPath(self):
        linear = np.arange(self.N)
        self.rg.shuffle(linear)
        return self.calcE(linear), linear
        
    def step(self):
        for i in range(500):
            e_prime, p = self.trySwap()
            e = self.calcE(self.path)
            if e_prime < e or self.rg.random() < np.exp((e - e_prime) / self.T):
                self.path = p

            e_prime, p = self.tryFlip()
            e = self.calcE(self.path)
            if e_prime < e or self.rg.random() < np.exp((e - e_prime) / self.T):
                self.path = p

        self.T *= 0.9

    # Returns indices of circular path
    def getMap(self):
        return np.append(self.path, self.path[0])

    # Calculate length of path
    def calcE(self, path):
        a = np.roll(self.nodes[path], 1, axis = 0)
        b = a - self.nodes[path]
        c = np.multiply(b, b)
        d = np.sum(c, 1)
        e = np.sqrt(d)
        return sum(e)

    def swap(self, a, b):
        self.path[a], self.path[b] = self.path[b], self.path[a]

    # swap two random nodes on virtual path and return new path
    def trySwap(self):
        ind = self.rg.integers(0, high=self.N, size=2)
        pathCopy = np.copy(self.path)
        self.path[ind[0]], self.path[ind[1]] = self.path[ind[1]], self.path[ind[0]]
        return self.calcE(pathCopy), pathCopy

    def tryFlip(self):
        ind = self.rg.integers(0, high=self.N, size=2)
        pathCopy = np.copy(self.path)
        pathCopy[ind[0]:ind[1]] = np.flip(pathCopy[ind[0]:ind[1]])
        return self.calcE(pathCopy), pathCopy


nNodes = 300
tour = tour(nNodes)
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 2)
axLeft = fig.add_subplot(gs[:,0])
axRight = fig.add_subplot(gs[:,1])

tourPlot, = axLeft.plot(tour.nodes[tour.getMap(),0], tour.nodes[tour.getMap(),1])
tmpPlot, = axRight.plot([],[])
axRight.set_xlim(0,1)
axRight.set_ylim(0,nNodes*0.6)
nFrames = 400
times = []
energy = []
def update(time):
    global tour
    tour.step()
    times.append(time/nFrames)
    energy.append(tour.calcE(tour.path))
    tourPlot.set_data(tour.nodes[tour.getMap(),0], tour.nodes[tour.getMap(),1])
    tmpPlot.set_data(times, energy)


animation = FuncAnimation(fig, update, frames=range(nFrames), interval=10, repeat=False)


plt.show()


