import numpy as np
import random as random
from progress.bar import Bar


# Loading bar for progress tracking
class CustomBar(Bar):
    message = 'Loading'
    fill = '#'
    suffix = '%(percent).1f%% - %(eta)ds'


# Creates and manages individual electron instances
class Electrons:

    # Arguments by order:
    # count: number of electrons
    # grid: Voltage field
    # size: array of size two defining the grid dimensions in meters
    # step_func: the step function the internal ODE solver will use
    # interpolation method used
    def __init__(self, count, grid, size, step_func, interpolation):
        self.count = count

        self.electrons = []

        for i in range(count):
            self.electrons.append(Electron(step_func, interpolation, grid, size))

    def solve(self, max_iterations, step_size):
        bar = CustomBar(max=self.count)
        for i in range(self.count):
            self.electrons[i].solve(max_iterations, step_size, )
            bar.next()

        bar.finish()

    def plot(self, axis, scale):
        for i in range(self.count):
            self.electrons[i].plot(axis, scale)


# constant
e_mc = 1.76 * 10 ** 11


# Electron instance
class Electron:

    def __init__(self, step_func, interpolation, grid, size):
        # Generate random angle
        angle = -np.pi/2 + random.random() * np.pi
        # TODO: Initial velocity is not working, i.e. way to big compared to other accelerations
        init_energy = 0#10 ** 6
        # Generate x,y velocity from angle
        vel = np.array([np.cos(angle) * init_energy, np.sin(angle) * init_energy])

        # Debug initial velocity
        #print('init velocity: ', vel)

        # Random position, according to task description
        pos = np.array([0, random.random() * 0.3 + 0.6])

        # Init y, add y_0
        self.y = []
        self.y.append(np.array([pos, vel]))

        #print(self.y)

        # init t, add t_0
        self.t = []
        self.t.append(0)

        # print(self.y)

        self.step_func = step_func
        self.interpolation = interpolation
        self.grid = grid
        self.size = size

        self.delta = np.array([1 / (np.shape(grid)[0]), 1 / (np.shape(grid)[1])])

    def df_dt(self, tn, pos):
        # Decreased delta yields more accurate derivative of grid position
        s_x = self.delta[0]
        s_y = self.delta[1]
        x = pos[0]
        y = pos[1]

        # negative step in x direction
        x_n = x - s_x
        # positive step in x direction
        x_p = x + s_x
        # negative step in y direction
        y_n = y - s_y
        # positive step in y direction
        y_p = y + s_y

        # Calculate derivative
        df_dx = 1. / (2 * s_x) * (self.interpolation(self.grid, [x_p, y]) - self.interpolation(self.grid, [x_n, y]))
        df_dy = 1. / (2 * s_y) * (self.interpolation(self.grid, [x, y_p]) - self.interpolation(self.grid, [x, y_n]))

        # TODO: Not sure about this, trying to adjust for scale since we obtain m/s^2 but our domain is 0.01m
        # Adjust for scaling
        df_dx /= self.size[0]
        df_dy /= self.size[1]

        acc = np.array([df_dx * e_mc, df_dy * e_mc])
        return acc

    # Simple ODE solver with special break condition
    def solve(self, max_iterations, step_size):

        for n in range(max_iterations - 1):
            self.y.append(self.step_func(self.t[n], self.y[n], step_size, self.df_dt))
            self.t.append(self.t[n] + step_size)

            # Break loop when electron exits grid space
            if self.y[n + 1][0][0] < 0 or self.y[n + 1][0][0] > 1 or self.y[n + 1][0][1] < 0 or self.y[n + 1][0][1] > 1:
                break

    def plot(self, axis, scale):
        self.y = np.array(self.y)
        #Debugging:
        #print('positions:', self.y[:, 0, :])
        #print('velocities:', self.y[:, 1, :])

        axis.scatter(self.y[:, 0, 0] * scale, self.y[:, 0, 1] * scale, s=1)
