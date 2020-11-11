import numpy as np
import matplotlib.pyplot as plt


# General Forward Euler implementation for two ODE's with dependence
def forward_euler(f_prime, f_init, g_prime, g_init, h, n):
    f_history = np.zeros(n)
    g_history = np.zeros(n)

    f_history[0] = f_init
    g_history[0] = g_init

    for i in range(1, n):
        f_history[i] = f_history[i - 1] + f_prime(f_history[i - 1], g_history[i - 1]) * h
        g_history[i] = g_history[i - 1] + g_prime(g_history[i - 1], f_history[i - 1]) * h

    return f_history, g_history


# General Runge Kutta implementation for two ODE's with dependence
def runge_kutta(f_prime, f_init, g_prime, g_init, h, n):
    f_history = np.zeros(n)
    g_history = np.zeros(n)

    f_history[0] = f_init
    g_history[0] = g_init

    for i in range(1, n):
        f_mid = f_history[i - 1] + 0.5 * h * f_prime(f_history[i - 1], g_history[i - 1])
        g_mid = g_history[i - 1] + 0.5 * h * g_prime(g_history[i - 1], f_history[i - 1])

        f_history[i] = \
            f_history[i - 1] + f_prime(f_mid, g_mid) * h

        g_history[i] = \
            g_history[i - 1] + g_prime(g_mid, f_mid) * h

    return f_history, g_history


    # General Runge Kutta 4th order implementation for two ODE's with dependence
    def runge_kutta_fourth(f_prime, f_init, g_prime, g_init, h, n):
        f_history = np.zeros(n)
        g_history = np.zeros(n)

        f_history[0] = f_init
        g_history[0] = g_init

        for i in range(1, n):
            f_k1 = h * f_prime(f_history[i - 1], g_history[i - 1])
            g_k1 = h * g_prime(g_history[i - 1], f_history[i - 1])

            f_k2 = h * f_prime(f_history[i - 1] + f_k1 / 2, g_history[i - 1] + g_k1 / 2)
            g_k2 = h * g_prime(g_history[i - 1] + g_k1 / 2, f_history[i - 1] + f_k1 / 2)

            f_k3 = h * f_prime(f_history[i - 1] + f_k2 / 2, g_history[i - 1] + g_k2 / 2)
            g_k3 = h * g_prime(g_history[i - 1] + g_k2 / 2, f_history[i - 1] + f_k2 / 2)

            f_k4 = h * f_prime(f_history[i - 1] + f_k3, g_history[i - 1] + g_k3)
            g_k4 = h * g_prime(g_history[i - 1] + g_k3, f_history[i - 1] + f_k3)

            f_history[i] = f_history[i - 1] + f_k1 / 6 + f_k2 / 3 + f_k3 / 3 + f_k4 / 6
            g_history[i] = g_history[i - 1] + g_k1 / 6 + g_k2 / 3 + g_k3 / 3 + g_k4 / 6

        return f_history, g_history


# Define Differential Equations with fixed given parameters
def mice_prime(number_of_mice, number_of_foxes, birth_rate=2, kmf=0.02):
    return number_of_mice * birth_rate - number_of_foxes * number_of_mice * kmf


def fox_prime(number_of_foxes, number_of_mice, death_rate=1.06, kfm=0.01):
    return number_of_mice * number_of_foxes * kfm - number_of_foxes * death_rate


# Perform calculations with parameters
mice_euler, fox_euler = forward_euler(mice_prime, 100, fox_prime, 15, 0.01, 3000)
mice_kutta, fox_kutta = runge_kutta(mice_prime, 100, fox_prime, 15, 0.01, 3000)

# Plotting
fig, axs = plt.subplots(2, 1)

axs[0].plot(mice_euler)
axs[0].plot(fox_euler)
axs[0].plot(mice_kutta)
axs[0].plot(fox_kutta)
axs[0].legend(['Mice Euler', 'Foxes Euler', 'Mice Kutta', 'Foxes Kutta'], loc=1)
axs[1].scatter(mice_euler, fox_euler, s=0.1)
axs[1].scatter(mice_kutta, fox_kutta, s=0.1)
axs[1].legend(['Euler', 'Kutta'], loc=1)
axs[0].set_title("Runge Kutta / Euler Method comparison with stepsize 0.01")

# Increment Stepsize to make error visible, decrease number of iterations by same factor to have equal number of cycles
mice_kutta, fox_kutta = runge_kutta(mice_prime, 100, fox_prime, 15, 0.1, 300)
mice_kutta_4, fox_kutta_4 = runge_kutta_fourth(mice_prime, 100, fox_prime, 15, 0.1, 300)

fig, axs = plt.subplots(2, 1)

axs[0].plot(mice_kutta)
axs[0].plot(fox_kutta)
axs[0].plot(mice_kutta_4)
axs[0].plot(fox_kutta_4)
axs[0].legend(['Mice Kutta', 'Foxes Kutta', 'Mice Kutta 4', 'Foxes Kutta 4'], loc=1)
axs[1].scatter(mice_kutta, fox_kutta, s=2)
axs[1].scatter(mice_kutta_4, fox_kutta_4, s=2)
axs[1].legend(['Kutta', 'Kutta 4'], loc=1)
axs[0].set_title("Runge Kutta / Runge Kutta 4th order comparison with stepsize 0.1")

plt.show()
