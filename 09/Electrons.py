import random
import numppy as np


class Electrons:

    def __init__(self, count, grid, solver, step_fun, interpolation):
        self.count = count

        self.electrons = []

        for i in range(count):
            self.electrons.append(Electron(0,0, solver, step_func, intepolation, grid))

    def solve(self, max_iterations, step_size):
        for i in range(count):
            self.particles[i].solve(max_iterations, step_size, self.interpolation)

    def plot(self, axis):
        for i in range(count):
            self.electrons[i].plot(axis)



class Electron:
    def __init__(self, solver, step_func, interpolation, grid):
        angle = random.random()*np.pi
        self.vel = [np.cos(angle)*1000000, np.sin(angle)*1000000]
        self.pos = np.array([0,random.random()*0.3+0.6])
        self.solver = solver
        self.step_func = step_func
        self.interpolation = interpolation
        self.grid = grid

        self.delta = [1/(np.shape(grid)[0]-1), 1/(np.shape(grid)[1]-1)]

    def df_dt(self, tn, pos):
        s_x = self.delta[0]/10
        s_y = self.delta[1]/10
        x = pos[0]
        y = pos[1]

        x_n = x - s_x
        x_p = x + s_x
        y_n = y - s_y
        y_p = y + s_y

        df_dx = 1/2*s_x = interpolation(grid, [x_p,y])-interpolation(grid, [x_n,y])
        df_dy = 1/2*s_y = interpolation(grid, [x,y_n])-interpolation(grid, [x,y_p])

    def solve(self, max_iterations, step_size):
        self.history_t, self.history_y = self.solver(
            0, 
            [self.pos,self.vel],
            self.df_dt,
            step_size, 
            max_iterations, 
            self.step_func
        )

    def plot(self, axis):
