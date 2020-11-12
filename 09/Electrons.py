import numpy as np
import random as random
from progress.bar import Bar


# Loading bar for progress tracking
class CustomBar(Bar):
    message = 'Loading'
    fill = '#'
    suffix = '%(percent).1f%% - %(eta)ds'


# Creates and manages indivial electron instances
class Electrons:

    def __init__(self, count, grid, solver, step_func, interpolation):
        self.count = count

        self.electrons = []

        for i in range(count):
            self.electrons.append(Electron(solver, step_func, interpolation, grid))

    def solve(self, max_iterations, step_size):
        bar = CustomBar(max=self.count)
        for i in range(self.count):
            self.electrons[i].solve(max_iterations, step_size,)
            bar.next()

        bar.finish()

    def plot(self, axis, scale):
        for i in range(self.count):
            self.electrons[i].plot(axis, scale)


e_mc = 1.76*10**11


# Electron instance
class Electron:

    def __init__(self, solver, step_func, interpolation, grid):
        # Generate random angle
        angle = random.random()*np.pi
        print(angle)
        init_energy = 10**6
        # Generate x,y velocity from angle
        vel = [np.cos(angle)*init_energy, np.sin(angle)*init_energy]
        print(vel)
        # Random position, according to task description
        pos = np.array([0, random.random()*0.3+0.6])

        # Init y, add y_0
        self.y = []
        self.y.append([pos, vel])

        # init t, add t_0
        self.t = []
        self.t.append(0)

        #print(self.y)

        self.solver = solver
        self.step_func = step_func
        self.interpolation = interpolation
        self.grid = grid

        self.delta = [1/(np.shape(grid)[0]-1), 1/(np.shape(grid)[1]-1)]

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
        df_dx = 1./(2*s_x) * (self.interpolation(self.grid, [x_p, y])-self.interpolation(self.grid, [x_n, y]))
        df_dy = 1./(2*s_y) * (self.interpolation(self.grid, [x, y_p])-self.interpolation(self.grid, [x, y_n]))

        return np.array([-df_dx*e_mc, -df_dy*e_mc])

    # Simple ODE solver with special break condition
    def solve(self, max_iterations, step_size):
 
        for n in range(max_iterations - 1):
            self.y.append(self.step_func(self.t[n], self.y[n], step_size, self.df_dt))
            self.t.append(self.t[n] + step_size)

            # Break loop when electron exits grid space
            if self.y[n+1][0][0] < 0 or self.y[n+1][0][0] > 1 or self.y[n+1][0][1] < 0 or self.y[n+1][0][1] > 1:
                break

    def plot(self, axis, scale):
        self.y = np.array(self.y)
        axis.plot(self.y[:, 0, 0]*scale, self.y[:, 0, 1]*scale)