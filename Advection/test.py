import numpy as np
from scipy import ndimage

a = np.array([
    [1,2,3,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]
])

b = ndimage.convolve(a, np.array([[0,0,1],[0,0,0],[0,0,0]]).T, mode="wrap")
print(a)
print(b)