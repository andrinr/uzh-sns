import numpy as np
import matplotlib.pyplot as plt


# Parameters
shape = (512, 512)

max_iterations = 100

# regular
center = (-2, -1.5)
zoom = 3

# spirals
#center = (-.7435669, .1314023)
#zoom = .001

# Initialization
pixels = np.zeros(shape)


# Calculation
def escape(x, y):

    C = complex(x,y)
    Z = C
    iterations = 0

    while Z.real < 2 and Z.imag < 2 and iterations < max_iterations:
        Z = Z*Z + C
        iterations += 1

    return iterations


def normalize(x, y):
    return x/shape[0], y/shape[1]


def mandelbrot_space(x, y):
    return zoom*x+center[0], zoom*y+center[1]


for x in range(shape[0]):
    for y in range(shape[1]):
        x_norm, y_norm = normalize(x, y)
        x_mandelbrot, y_mandelbrot = mandelbrot_space(x_norm, y_norm)
        pixels[y, x] = escape(x_mandelbrot, y_mandelbrot)


# Plot
fig, ax = plt.subplots()
plt.imshow(pixels,cmap=plt.get_cmap('PiYG'))
plt.show()
