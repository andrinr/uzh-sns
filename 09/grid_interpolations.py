import numpy as np
import matplotlib.pyplot as plt

def get_coords(shape, coord):
    delta = [1/(shape[0]-1), 1/(shape[1]-1)]

    x = coord[0] / delta[0]
    y = coord[1] / delta[1]

    u = x % 1
    v = y % 1

    x = int(x)
    y = int(y)

    return x, y, u, v


def bilinear(grid, coord):
    x, y, u, v = get_coords(np.shape(grid), coord)

    return grid[x,y] * (1-u) * (1-v) + grid[x+1,y] * u * (1-v) + grid[x,y+1] * (1-u) *  v + grid[x+1,y+1] * u * v

def bicubic(grid, coord):

    x, y, u, v = get_coords(np.shape(grid), coord)

    g00 = grid[x,y]
    g01 = grid[x,y+1]
    g10 = grid[x+1,y]
    g11 = grid[x+1,y+1]

    dy00 = deriv(grid, [x, y], 1)
    dy01 = deriv(grid, [x, y+1], 1)
    dy10 = deriv(grid, [x+1, y], 1)
    dy11 = deriv(grid, [x+1, y+1], 1)

    dx00 = deriv(grid, [x, y], 0)
    dx01 = deriv(grid, [x, y+1], 0)
    dx10 = deriv(grid, [x+1, y], 0)
    dx11 = deriv(grid, [x+1, y+1], 0)

    dxy00 = cross_deriv(grid, [x,y])
    dxy01 = cross_deriv(grid, [x,y+1])
    dxy10 = cross_deriv(grid, [x+1,y])
    dxy11 = cross_deriv(grid, [x+1,y+1])
    
    A = np.matrix([
        [g00, g01, dy00, dy01],
        [g10, g11, dy10, dy11],
        [dx00, dx01, dxy00, dxy01],
        [dx10, dx11, dxy10, dxy11],
    ])

    M = np.matrix([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [-3, 3, -2, -1],
        [2, -2, 1, 1]
    ])

    X = np.matrix([[1, u, u*u, u*u*u]])
    Y = np.matrix([[1], [v], [v*v], [v*v*v]])

    return X * M * A * M.T * Y

def deriv(grid, coord, axis):
    x = coord[0]
    y = coord[1]
    x_p = min(x+1, np.shape(grid)[0]-1)
    x_n = max(x-1, 0)

    y_p = min(y+1, np.shape(grid)[1]-1)
    y_n = max(y-1, 0)

    if axis == 0:
        return grid[x_p, y] - grid[x_n, y]
    else:
        return  grid[x, y_p] - grid[x, y_n]

def cross_deriv(grid, coord):
    x = coord[0]
    y = coord[1]

    y_p = min(y+1, np.shape(grid)[1]-1)
    y_n = max(y-1, 0)

    p1 = deriv(grid, [x,y_n], 0)
    p2 = deriv(grid, [x,y_p], 0)
    return p2-p1


# Run this script to see the testing plots

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(1, 3)

# Line plots
raw_ax = fig.add_subplot(gs[:,0])
linear_ax = fig.add_subplot(gs[:,1])
cubic_ax = fig.add_subplot(gs[:,2])

N1 = 10
N2 = 100

noise = np.random.rand(N1,N1)

linear = np.zeros((N2,N2))

cubic = np.zeros((N2,N2))

for i in range(N2):
    for j in range(N2):
        linear[i,j] = bilinear(noise,[1/N2*i,1/N2*j])

for i in range(N2):
    for j in range(N2):
        cubic[i,j] = bicubic(noise,[1/N2*i,1/N2*j])

raw_ax.imshow(noise,cmap="plasma")
linear_ax.imshow(linear,cmap="plasma")
cubic_ax.imshow(cubic,cmap="plasma")

plt.show()