import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

class Eliptic:
    
    def __init__(self, N, P, boundary):
        self.N = N
        self.boundary = boundary
        self.P = P

        # Make kernel
        self.kernel = np.array([[0,1,0],
                                [1,-4,1],
                                [0,1,0]])

        # time and error
        self.error = []
        self.time = []

         # Create checkerboard boolean Map
        self.checkerboard = np.full((N,N),False)
        self.checkerboard[::2,::2] = True   
        self.checkerboard[1::2,1::2] = True

    
    # Solver step
    def step(self, iteration):
        # Apply kernel, multiply by boundary and checkerboard
        change_checkerboard = 0.25 * np.multiply(ndimage.convolve(self.P, self.kernel, mode='constant'), self.boundary)[self.checkerboard]
        self.P[self.checkerboard] += change_checkerboard
    
        # Apply kernel, multiply by boundary and inverse checkerboard
        change_i_checkerboard = 0.25 * np.multiply(ndimage.convolve(self.P, self.kernel, mode='constant'), self.boundary)[~self.checkerboard]
        self.P[~self.checkerboard] += change_i_checkerboard

        # Get maximum error over domain
        current_error = max(np.abs(np.max(change_checkerboard)), np.abs(np.max(change_i_checkerboard)))

        # Store error and time
        self.error.append(np.log(current_error))
        self.time.append(iteration)

        return current_error


    def solve(self, max_error, max_steps=1000):
        i = 0
        while True:
            i += 1
            error = self.step(i)

            if error < max_error or i > max_steps:
                return

    def plot(self, axis):
        axis.imshow(self.P, cmap="plasma")