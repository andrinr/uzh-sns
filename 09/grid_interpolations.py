import numpy as np

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

    np.array([
        
    ])
    return

def derivative(grid, coord, axis):
    if axis == 0:
        return grid[coord[0]+1,coord[1]] - grid[coord[0]-1,coord[1]]
    else:
        return grid[coord[0],coord[1]+1] - grid[coord[0],coord[1]-1]

print(bilinear(np.zeros((5,4)),[0.99,0.99]))