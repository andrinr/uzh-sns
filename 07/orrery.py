
import pandas as pd
import numpy as np


def leap_frog_step(tn, yn, h, dfdt):

    vel_half = yn[0] + 0.5 * h * dfdt(tn, yn)

    pos_1 = y[1] - h *

    return


def ode_solver(t0, y0, df_func, h, n_steps, solver_step_func):

    t = np.zeros(n_steps)
    y = np.zeros(n_steps)
    t[0] = t0
    y[0] = y0

    for n in range(n_steps-1):
        y[n+1] = solver_step_func(t[n], y[n], h, df_func)
        t[n+1] = t[n] + h

    return t, y


df = pd.read_csv("SolSystData.dat", sep=',', header=None,
                     names=['name', 'm', 'x', 'y', 'z', 'vx', 'vy', 'vz'])

print(df)