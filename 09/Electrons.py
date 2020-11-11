import numpy as np
import random as random

# Creates and manages indivial electron instances
class Electrons:

    def __init__(self, count, grid, solver, step_func, interpolation):
        self.count = count

        self.electrons = []

        for i in range(count):
            self.electrons.append(Electron(solver, step_func, interpolation, grid))

    def solve(self, max_iterations, step_size):
        for i in range(self.count):
            self.electrons[i].solve(max_iterations, step_size,)

    def plot(self, axis, scale):
        for i in range(self.count):
            self.electrons[i].plot(axis, scale)


# Electron instance
class Electron:

    def __init__(self, solver, step_func, interpolation, grid):
        # Generate random angle
        angle = random.random()*np.pi
        # TODO: Conversion
        # Generate x,y velocity from angle
        vel = [np.cos(angle), np.sin(angle)]
        # Random position, according to task description
        pos = np.array([0,random.random()*0.3+0.6])

        # Init y, add y_0
        self.y = []
        self.y.append([pos,vel])

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
        # Decreased delta yields more accuarte derivate of grid position
        s_x = self.delta[0]/100
        s_y = self.delta[1]/100
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

        # Calcualte derivates
        df_dx = 1./(2*s_x) * self.interpolation(self.grid, [x_p,y])-self.interpolation(self.grid, [x_n,y])
        df_dy = 1./(2*s_y) * self.interpolation(self.grid, [x,y_n])-self.interpolation(self.grid, [x,y_p])

        return np.array([df_dx, df_dy])

    # Simple ODE solver with special break condition
    def solve(self, max_iterations, step_size):
 
        for n in range(max_iterations - 1):
            self.y.append(self.step_func(self.t[n], self.y[n], step_size, self.df_dt))
            self.t.append( self.t[n] + step_size )

            if self.y[n+1][0][0] < 0 or self.y[n+1][0][0] > 1 or self.y[n+1][0][1] < 0 or self.y[n+1][0][1] > 1:
                break



    def plot(self, axis, scale):
        print(self.y[:][0][0]*scale)
        print(self.y[:][0][1]*scale)
        #print(self.y)
        axis.plot(self.y[:][0][0]*scale, self.y[:][0][1]*scale)