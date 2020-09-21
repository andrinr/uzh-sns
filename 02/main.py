import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


planets = pd.read_csv('planets.csv')
print(planets.head())


# define the accuracy
acc = 0.001


# recursive approach
def newton_kepler(f, f_derivative, guess, accuracy, mean_anomaly, eccentricity):
    # exit if desired accuracy is reached
    if np.abs(f(guess, mean_anomaly, eccentricity)) < accuracy:
        return guess

    # make new (hopefully) improved guess
    new_guess = guess - f(guess, mean_anomaly, eccentricity) / f_derivative(guess, eccentricity)

    # recursive call
    return newton_kepler(
        f,
        f_derivative,
        new_guess,
        accuracy,
        mean_anomaly,
        eccentricity
    )


def kepler(eccentric_anomaly, mean_anomaly, eccentricity):
    return eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly) - mean_anomaly


def kepler_derivative(eccentric_anomaly, eccentricity):
    return 1 - eccentricity * np.cos(eccentric_anomaly)


def orbit(mean_anomaly, eccentricity, semi_major_axis, accuracy):
    semi_minor_axis = semi_major_axis * np.sqrt(1 - eccentricity)

    eccentric_anomaly = newton_kepler(kepler, kepler_derivative, 0, accuracy, mean_anomaly, eccentricity)

    x = semi_major_axis * (np.cos(eccentric_anomaly) - eccentricity)
    y = semi_minor_axis * np.sin(eccentric_anomaly)

    return x, y


# Plotting
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')


def init():
    plt.cla()
    ax.set_xlim(-6000, 6000)
    ax.set_ylim(-6000, 6000)
    return ln,


def update(frame):
    xdata = []
    ydata = []

    for index, planet in planets.iterrows():
        x, y = orbit(planet['orbital_velocity']*frame, planet['orbital_eccentricity'], planet['semi_major_axis'], 0.0001)
        xdata.append(x)
        ydata.append(y)

    ln.set_data(xdata, ydata)
    return ln,


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 1024), init_func=init, blit=True, interval=40)

plt.show()
