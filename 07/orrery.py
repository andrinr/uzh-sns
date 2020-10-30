import pandas as pd
import numpy as np
from progress.bar import Bar
import matplotlib.pyplot as plt


# Commonly referenced:
def leap_frog_step_legacy(tn, yn, h, df_dt):

    vel_half = yn[1] + 0.5 * h * df_dt(tn, yn[0])

    pos = yn[0] + h * vel_half

    vel = vel_half + 0.5 * h * df_dt(tn + 1, pos)

    return [pos, vel]


# Introduced in the lecture:
def leap_frog_step(tn, yn, h, df_dt):

    pos_half = yn[0] + 0.5 * h * yn[1]

    vel = yn[1] + h * df_dt(tn+1, pos_half)

    pos = pos_half + 0.5 * h * vel

    return [pos, vel]


# Loading bar for progress tracking
class CustomBar(Bar):
    message = 'Loading'
    fill = '.'
    suffix = '%(percent).1f%% - %(eta)ds'


# General ODE solver
def ode_solver(t0, y0, df_dt, h, n_steps, solver_step_func):
    t = np.zeros(n_steps)
    y = np.zeros((n_steps,) + np.shape(y0))
    t[0] = t0
    y[0] = y0

    bar = CustomBar(max=n_steps)
    for n in range(n_steps - 1):
        y[n+1] = solver_step_func(t[n], y[n], h, df_dt)
        t[n+1] = t[n] + h

        bar.next()

    bar.finish()

    return t, y


# Read dataset
df = pd.read_csv("SolSystData.dat", sep=',', header=None,
                 names=['name', 'm', 'x', 'y', 'z', 'vx', 'vy', 'vz'])
n_planets = 9
df = df.loc[0:n_planets]

# Extract values and put into desired data types
positions_0 = np.array(df[['x', 'y', 'z']])
velocities_0 = np.array(df[['vx', 'vy', 'vz']])
y_0 = [positions_0, velocities_0]

m = np.array(df['m'])
names = np.array(df['name'])
# Constant
k = 0.01720209895


# Planet accelerations
def df_dt_planets(t, positions, masses=m):
    n = len(positions)
    acceleration = np.zeros((n, 3))

    # planet one
    for p1 in range(n):
        # planet two, skip doubles and self
        for p2 in range(p1):
            # Calculate vector from current planet i to planet j
            distance_vector = positions[p2] - positions[p1]
            # Calculate euclidean distance, take power of 3, take inverse
            ir3 = 1. / np.power(np.linalg.norm(distance_vector), 3)

            # Newtons law of universal gravity
            force = distance_vector * masses[p1] * masses[p2] * ir3 * k * k

            acceleration[p1] += force * 1. / masses[p1]
            acceleration[p2] -= force * 1. / masses[p2]

    return acceleration


step = 100
fig1 = plt.figure()
fig1, axs1 = plt.subplots(2, 2)

print("Processing 1 year of the solar system:")
timeline, planets = ode_solver(0, y_0, df_dt_planets, 0.01, 365*100, leap_frog_step)

for i in range(5):
    axs1[0][0].plot(planets[::step, 0, i, 0], planets[::step, 0, i, 1])
    axs1[1][0].plot(planets[::step, 0, i, 0], planets[::step, 0, i, 2])

fig2, axs2 = plt.subplots(3, 1)
for i in range(5):
    axs2[0].set_title("X positions")
    axs2[0].plot(timeline[::step], planets[::step, 0, i, 0])
    axs2[1].set_title("Y positions")
    axs2[1].plot(timeline[::step], planets[::step, 0, i, 1])
    axs2[2].set_title("Z positions")
    axs2[2].plot(timeline[::step], planets[::step, 0, i, 2])

print("Processing 100 years of the solar system with lower precision:")
timeline, planets = ode_solver(0, y_0, df_dt_planets, 1, 365*100, leap_frog_step)

for i in range(n_planets):
    axs1[0][1].plot(planets[::step, 0, i, 0], planets[::step, 0, i, 1])
    axs1[1][1].plot(planets[::step, 0, i, 0], planets[::step, 0, i, 2])

plt.legend(names, loc=1)

fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
for i in range(n_planets):
    ax.plot(planets[::step, 0, i, 0], planets[::step, 0, i, 1], planets[::step, 0, i, 2])

plt.legend(names, loc=1)

# Diagnosis plots of individual coordinates, positions and velocities
fig3, axs3 = plt.subplots(3, 1)
# Add spacing between subplots

# Outer solar system
for i in range(4):
    axs3[0].set_title("X positions")
    axs3[0].plot(timeline[::step], planets[::step, 0, i+5, 0])
    axs3[1].set_title("Y positions")
    axs3[1].plot(timeline[::step], planets[::step, 0, i+5, 1])
    axs3[2].set_title("Z positions")
    axs3[2].plot(timeline[::step], planets[::step, 0, i+5, 2])

plt.legend(names, loc=1)
plt.show()
