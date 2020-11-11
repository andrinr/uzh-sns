import numpy as np
import random as random


class Electrons:

    def __init__(self, count, grid, solver, step_func, interpolation):
        self.count = count

        self.electrons = []

        for i in range(count):
            self.electrons.append(Electron(solver, step_func, interpolation, grid))

    def solve(self, max_iterations, step_size):
        for i in range(self.count):
            self.electrons[i].solve(max_iterations, step_size,)

    def plot(self, axis):
        for i in range(self.count):
            self.electrons[i].plot(axis)



class Electron:

    def __init__(self, solver, step_func, interpolation, grid):
        angle = random.random()*np.pi
        # TODO: Conversion
        vel = [np.cos(angle), np.sin(angle)]
        pos = np.array([0,random.random()*0.3+0.6])
        self.y = []
        self.y.append([pos,vel])

        self.t = []
        self.t.append(0)

        #print(self.y)

        self.solver = solver
        self.step_func = step_func
        self.interpolation = interpolation
        self.grid = grid

        self.delta = [1/(np.shape(grid)[0]-1), 1/(np.shape(grid)[1]-1)]

    def df_dt(self, tn, pos):
        s_x = self.delta[0]/100
        s_y = self.delta[1]/100
        x = pos[0]
        y = pos[1]

        x_n = x - s_x
        x_p = x + s_x
        y_n = y - s_y
        y_p = y + s_y

        #print(pos)

        df_dx = 1./(2*s_x) * self.interpolation(self.grid, [x_p,y])-self.interpolation(self.grid, [x_n,y])
        df_dy = 1./(2*s_y) * self.interpolation(self.grid, [x,y_n])-self.interpolation(self.grid, [x,y_p])

        return np.array([df_dx, df_dy])

    def solve(self, max_iterations, step_size):
 
        for n in range(max_iterations - 1):
            self.y.append(self.step_func(self.t[n], self.y[n], step_size, self.df_dt))
            self.t.append( self.t[n] + step_size )

            if self.y[n+1][0][0] < 0 or self.y[n+1][0][0] > 1 or self.y[n+1][0][1] < 0 or self.y[n+1][0][1] > 1:
                break



    def plot(self, axis):
        print(self.y)
        axis.plot(self.y[:][0][0], self.y[:][0][1])