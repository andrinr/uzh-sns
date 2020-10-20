import numpy as np
import matplotlib.pyplot as plt


def leap_frog_spring(q_init, p_init, h, n):
    q = np.zeros(n)
    p = np.zeros(n)

    q[0] = q_init
    p[0] = p_init

    for i in range(1, n):
        q_half = q[i - 1] + 0.5 * h * p[i - 1]
        p[i] = p[i - 1] - h * q_half
        q[i] = q_half + 0.5 * h * p[i]

    return q, p


def leap_frog_pendulum(q_init, p_init, h, n, epsilon):
    q = np.zeros(n)
    p = np.zeros(n)

    q[0] = q_init
    p[0] = p_init

    for i in range(1, n):
        q_half = q[i - 1] + 0.5 * h * p[i - 1]
        p[i] = p[i - 1] - h * epsilon * np.sin(q_half)
        q[i] = q_half + 0.5 * h * p[i]

    return q, p



# Plotting spring

q, p = leap_frog_spring(0, 1, 0.1, 100)
plt.scatter(q, p, 1)

q, p = leap_frog_spring(1, 1, 0.1, 100)
plt.scatter(q, p, 1)

q, p = leap_frog_spring(0, 0.75, 0.1, 100)
plt.scatter(q, p, 1)

q, p = leap_frog_spring(0.25, 0.25, 0.1, 100)
plt.scatter(q, p, 1)

# Plotting pendulum

q, p = leap_frog_pendulum(0.5, 0, 0.1, 500, 0.5)
plt.scatter(q, p, 1)

q, p = leap_frog_pendulum(1, 0, 0.1, 500, 0.5)
plt.scatter(q, p, 1)

q, p = leap_frog_pendulum(2, 0, 0.1, 500, 0.5)
plt.scatter(q, p, 1)

q, p = leap_frog_pendulum(3, 0, 0.1, 500, 0.5)
plt.scatter(q, p, 1)

plt.set(adjustable='box-forced', aspect='equal')

plt.show()