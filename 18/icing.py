import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import convolve

# Parameters
sqrtN = 200

rg = np.random.default_rng()

spin = np.sign(rg.random((sqrtN, sqrtN))-0.5)


kernel = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
])

T = 4
rg = np.random.default_rng()

# Fast but not necessarily accurate version (?)
# Makes use of parallel numpy / scipy operations
def updateFast(frame):
    global sqrtN, spin, kernel, rg, T
    # Steps that are not renderer, greatly increases efficiency
    for i in range(100):
        print("tmp: ", T)
        dE = np.zeros((sqrtN, sqrtN))
        convolve(spin, kernel, mode="wrap", output = dE)

        dE *= 2 * spin

        mask = dE < 0

        beta = 1. / T
        rand = rg.random((sqrtN, sqrtN))
        mask = np.logical_or(rand < np.exp(-beta * dE),  mask)
        
        # Only apply changes to small subset
        # Eror occurs when neighbours are picked, cannot be avoided because avoiding neighbours is not random anymore
        rand = rg.random((sqrtN, sqrtN))
        # The higher the compared value, the lower the accuracy
        mask = np.logical_and(rand<0.03, mask)
        
        spin[mask] = -spin[mask]

        T -= 0.01 * T

    im.set_array(spin)

# Slow, as proposed in lecture
def updateSlow(frame):
    global sqrtN, spin, kernel, rg, T
    for i in range(1000):
        print("tmp: ", T)
        pos = rg.integers(low=0, high=sqrtN, size=2)
        dE = spin[pos[0], (pos[1] + 1) % sqrtN]
        dE += spin[pos[0], (pos[1] - 1) % sqrtN]
        dE += spin[(pos[0] + 1) % sqrtN, pos[1]]
        dE += spin[(pos[0] - 1) % sqrtN, pos[1]]
        
        dE *= 2 * spin[pos[0], pos[1]]

        mask = dE < 0

        beta = 1. / T
        rand = rg.random((sqrtN, sqrtN))
        mask = np.logical_or(rand < np.exp(-beta * dE),  mask)

        if dE < 0 or rg.random() < np.exp(-beta * dE):
            spin[pos[0], pos[1]] = - spin[pos[0], pos[1]]

        T -= 0.01 * T

    im.set_array(spin)


fig, axs = plt.subplots(1)
im = axs.imshow(spin)

# plotting
#animation = FuncAnimation(fig, updateFast, frames=range(1), interval=10, repeat=False)


plt.show()