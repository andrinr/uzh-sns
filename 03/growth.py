import numpy as np
import matplotlib.pyplot as plt


# logistic equation
def logistic(X_n, alpha):
    return alpha * X_n * (1 - X_n)


def growth(alpha = 2.3, intital = 0.5, iterations = 300, cutoff = 100):

    return_array = np.zeros((iterations-cutoff, 2))
    X = intital

    for j in range(iterations):
        # caclculate new X, X_{n+1}
        X = logistic(X, alpha)

        # only save values after the cutoff is exceeded
        if j >= cutoff:
            return_array[j-cutoff, :] = [alpha, X]

    return return_array

x_resolution = 2000
# init and declare array of alpha values, ranging between 1 and 4
# We omit [0,1] because all results are 0 anyways
alphas = np.linspace(1, 4, x_resolution)
iterations = 200
cutoff = 100
points = np.zeros((x_resolution, iterations-cutoff,2))

for i in range(x_resolution):
    points[i, :, :] = growth(alphas[i], 0.5, iterations, cutoff)


# plot obtained values, fractal behaviour
fig, ax = plt.subplots()
plt.scatter(points[:, :, 0].flatten(), points[:, :, 1].flatten(), 1, "#000", marker="^")


# growth

fig, axs = plt.subplots(2, 2)
x = np.linspace(0, 1, 100)

alphas = [2.75, 0.9, 3.2, 3.8]
initials = [0.5,0.8,0.5,0.3]
titles = [
    'Intersection convergence, a = 2.75',
    'Convergence to 0, a = 0.9',
    'Cyclical behaviour, a = 3.2',
    'Chaotic behaviour, a = 3.8'
]

# Plot four subplots with different characteristic behaviours
for index in range(4):
    axis = axs.flatten()[index]
    alpha = alphas[index]
    axis.set_title(titles[index])

    # y data from parabola
    y_1 = x * alpha * (1 - x)
    # y data from 45deg line
    y_2 = x

    axis.plot(x, y_1)
    axis.plot(x, y_2)

    n = 30
    # only interested in y values
    growth_y = growth(alpha, initials[index], n, 0)[:, 1]

    # init line plot data
    line_x = np.zeros(n*2)
    line_y = np.zeros(n*2)

    line_x[0] = 0.5
    line_y[0] = 0

    for i in range(1,n):
        # y = X_{n}
        # x = X_{n-1}
        line_x[2*i] = growth_y[i-1]
        line_y[2*i] = growth_y[i]
        # y = X_{n}
        # x = X_{n}
        line_x[2*i+1] = growth_y[i]
        line_y[2*i+1] = growth_y[i]

    axis.plot(line_x[2:],line_y[2:])


fig.tight_layout(pad=3.0)

plt.show()


