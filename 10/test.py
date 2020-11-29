import numpy as np
from scipy import ndimage

a = np.array([0,1,0,0])

b = np.roll(a,1)
print(a+b)