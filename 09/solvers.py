import numpy as np

# General ODE solver
def ode_solver(t0, y0, df_dt, h, n_steps, solver_step_func):
    t = np.zeros(n_steps)
    y = np.zeros((n_steps,) + np.shape(y0))
    t[0] = t0
    y[0] = y0

    for n in range(n_steps - 1):
        y[n+1] = solver_step_func(t[n], y[n], h, df_dt)
        t[n+1] = t[n] + h

    return t, y


# Leap Frog Step
def leap_frog_step(tn, yn, h, df_dt):

    pos_half = yn[0] + 0.5 * h * yn[1]

    vel = yn[1] + h * df_dt(tn+1, pos_half)

    pos = pos_half + 0.5 * h * vel

    return [pos, vel]


# General Runge Kutta 4th order implementation for two ODE's with dependence
def runge_kutta_fourth_step(tn, yn, h, df_dt):

    h_d2 = 0.5 * h

    k1 = h * df_dt(tn, yn[0])

    k2 = h * df_dt(tn + h_d2, yn[0] + h_d2*k1)

    k3 = h * df_dt(tn + h_d2, yn[0] + h_d2*k2)

    k4 = h * df_dt(tn + h, yn[0] + h*k3)

    vel = 1/6*(k1 + 2*k2 + 2*k3 + k4)

    pos = yn[0] + vel

    return [pos, vel]