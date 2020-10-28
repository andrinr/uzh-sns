
import pandas as pd
import numpy as np

# General leap frog integration
# y[0] = positions, y[1] = velocities
def leap_frog_step(tn, yn, h, df_dt):

    vel_half = yn[1] + 0.5 * h * df_dt(tn + 0.5, yn[0])

    pos = yn[0] + h * vel_half

    vel = vel_half + 0.5 * h * df_dt(tn + 1, pos)

    return [pos, vel]


# General ODE solver
def ode_solver(t0, y0, df_dt, h, n_steps, solver_step_func):

    t = np.zeros(n_steps)
    y = np.zeros( (n_steps,) + np.shape(y0))
    t[0] = t0
    y[0] = y0

    for n in range(n_steps-1):
        y[n+1] = solver_step_func(t[n], y[n], h, df_dt)
        t[n+1] = t[n] + h

    return t, y


# Read dataset
df = pd.read_csv("SolSystData.dat", sep=',', header=None,
                     names=['name', 'm', 'x', 'y', 'z', 'vx', 'vy', 'vz'])

# Extract values and put into desired datatypes
positions_0 = np.array(df[['x', 'y', 'z']])
velocities_0 = np.array(df[['vx', 'vy', 'vz']])
y_0 = [positions_0, velocities_0]
m = np.array(df['m'])


# Define planet velocities
def df_dt_planets(t, positions, masses=m):
    n = len(positions)
    # Init and allocate matrix
    forces = np.zeros((n, n, 3))

    # Perspective: planet i
    for i in range(n):
        for j in range(i):
            # Calculate vector from current planet i to planet j
            distance_vector = positions[j] - positions[i]
            # Calculate euclidean distance, take power of 3
            euclidean_distance_3 = np.power(np.linalg.norm(distance_vector), 3)
            print(distance_vector)
            # Final gravity formula
            forces[i][j] = masses[i] * masses[j] * 1 / euclidean_distance_3 * distance_vector

    # Make use of already calculated forces
    # By negative mirroring the matrix along the diagonal
    forces[np.triu_indices(n, 1)] = -forces[np.tril_indices(n, -1)]

    return forces


ode_solver(0, y_0, df_dt_planets, 0.1, 1000, leap_frog_step)

# Testing
# df_dt_planets(0, np.array([[1,2,3],[1,5,6],[125,54,4]]), np.array([1,1,1]))