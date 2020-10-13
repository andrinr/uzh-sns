import numpy as np
import matplotlib.pyplot as plt


def mice_prime(number_of_mice, number_of_foxes, birth_rate = 2, kmf = 0.02):
    return number_of_mice * birth_rate - number_of_foxes * number_of_mice * kmf


def fox_prime(number_of_foxes, number_of_mice, death_rate = 1.06, kfm = 0.01):
    return number_of_mice * number_of_foxes * kfm - number_of_foxes * death_rate


def forward_euler(f_prime, f_init, g_prime, g_init, h, n):

    f_history = np.zeros(n)
    g_history = np.zeros(n)

    f_history[0] = f_init
    g_history[0] = g_init

    for i in range(1, n):
        f_history[i] = f_history[i-1] + f_prime(f_history[i-1], g_history[i-1]) * h
        g_history[i] = g_history[i-1] + g_prime(g_history[i-1], f_history[i-1]) * h

    return f_history, g_history


def runge_kutta(f_prime, f_init, g_prime, g_init, h, n):

    f_history = np.zeros(n)
    g_history = np.zeros(n)

    f_history[0] = f_init
    g_history[0] = g_init

    for i in range(1, n):
        f_mid = f_history[i - 1] + 0.5 * h * f_prime(f_history[i - 1], g_history[i - 1])
        g_mid = g_history[i - 1] + 0.5 * h * g_prime(g_history[i - 1], f_history[i - 1])

        f_history[i] = \
            f_history[i - 1] + f_prime( f_mid, g_mid) * h

        g_history[i] = \
            g_history[i - 1] + g_prime(g_mid, f_mid) * h

    return f_history, g_history


fig, axs = plt.subplots(2, 1)

mice_euler, fox_euler = forward_euler(mice_prime, 100, fox_prime, 15, 0.001, 30000)
mice_kutta, fox_kutta = runge_kutta(mice_prime, 100, fox_prime, 15, 0.001, 30000)
axs[0].plot(mice_euler)
axs[0].plot(fox_euler)
axs[0].plot(mice_kutta)
axs[0].plot(fox_kutta)

axs[1].scatter(mice_euler, fox_euler, s=0.1)
axs[1].scatter(mice_kutta, fox_kutta, s=0.1)
plt.show()