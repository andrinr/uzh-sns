import numpy as np

# Init random generator
rg = np.random.default_rng()

class Particle:

    def __init__(self):
        self.p = rg.random((2))
        self.v = np.zeros((2))
        self.e = 0
        self.c = 0
        self.h = 0