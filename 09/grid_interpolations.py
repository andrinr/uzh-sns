import numpy as np
import matplotlib.pyplot as plt


# Get int x,y and fractions as u,v 
def get_coords(shape, coord):
    # We are fetching the lower left coordinate
    # Therefore we make sure it is lower and to the left
    # of the upper and left border
    delta = [1/(shape[0]-1), 1/(shape[1]-1)]

    x = coord[0] / delta[0]
    y = coord[1] / delta[1]

    # Get fractions
    u = x % 1
    v = y % 1

    # floor
    x = int(x)
    y = int(y)

    return x, y, u, v


# Bilinear integration
def bilinear(grid, coord):
    x, y, u, v = get_coords(np.shape(grid), coord)

    return grid[x, y] * (1-u) * (1-v) + grid[x+1, y] * u * (1-v) + grid[x, y+1] * (1-u) * v + grid[x+1, y+1] * u * v


# Bicubic integration with boundary conditions
# Slow performance, could be improved
def bicubic(grid, coord):

    shape = np.shape(grid)
    # clamp at boundary

    x, y, u, v = get_coords(shape, coord)

    # Clamp at boundary, assume grid is continuous on borders
    # Meaning a derivative of 0
    if x == shape[0]-1:
        x = shape[0]-2
        u = 0.999
    
    if y == shape[1]-1:
        y = shape[1]-2
        v = 0.999

    # grid values
    g00 = grid[x, y]
    g01 = grid[x, y+1]
    g10 = grid[x+1, y]
    g11 = grid[x+1, y+1]

    # Derivatives with respect to y
    dy00 = deriv(grid, [x, y], 1)
    dy01 = deriv(grid, [x, y+1], 1)
    dy10 = deriv(grid, [x+1, y], 1)
    dy11 = deriv(grid, [x+1, y+1], 1)

    # Derivatives with respect to x
    dx00 = deriv(grid, [x, y], 0)
    dx01 = deriv(grid, [x, y+1], 0)
    dx10 = deriv(grid, [x+1, y], 0)
    dx11 = deriv(grid, [x+1, y+1], 0)

    # Derivatives with respect to x and y
    # dxy** == dyx**
    dxy00 = cross_deriv(grid, [x, y])
    dxy01 = cross_deriv(grid, [x, y+1])
    dxy10 = cross_deriv(grid, [x+1, y])
    dxy11 = cross_deriv(grid, [x+1, y+1])
    
    # Build matrices
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

    # Matrix multiplication and reading fina value
    return (X * M * A * M.T * Y)[0, 0]


# Simple numerically approximated derivative
def deriv(grid, coord, axis):
    shape = np.shape(grid)
    x = coord[0]
    y = coord[1]
    # clamp at boundary
    x_p = min(x+1, shape[0]-1)
    x_n = max(x-1, 0)
    # clamp at boundary
    y_p = min(y+1, shape[1]-1)
    y_n = max(y-1, 0)

    # There is no divisor because distances are uniform
    if axis == 0:
        return (grid[x_p, y] - grid[x_n, y])
    else:
        return (grid[x, y_p] - grid[x, y_n])


# Simple numerically approximated cross derivative
def cross_deriv(grid, coord):
    x = coord[0]
    y = coord[1]

    y_p = min(y+1, np.shape(grid)[1]-1)
    y_n = max(y-1, 0)

    p1 = deriv(grid, [x, y_n], 0)
    p2 = deriv(grid, [x, y_p], 0)

    # There is no divisor because distances are uniform
    return (p2 - p1)
