import numpy as np
import matplotlib.pyplot as plt


def leap_frog_spring(q_init, p_init, h, n):
    q = np.zeros(n)
    p = np.zeros(n)

    q[0] = q_init
    p[0] = p_init

    for i in range(1, n):
        # half step velocity
        q_half = q[i - 1] + 0.5 * h * p[i - 1]
        # full step position
        p[i] = p[i - 1] - h * q_half
        # full step velocity
        q[i] = q_half + 0.5 * h * p[i]

    return q, p


def leap_frog_pendulum(q_init, p_init, h, n, epsilon):
    q = np.zeros(n)
    p = np.zeros(n)

    q[0] = q_init
    p[0] = p_init

    for i in range(1, n):
        # half step velocity
        q_half = q[i - 1] + 0.5 * h * p[i - 1]
        # full step angle
        p[i] = p[i - 1] - h * epsilon * np.sin(q_half)
        # full step velocity
        q[i] = q_half + 0.5 * h * p[i]

    return q, p


fig, axs = plt.subplots(1, 2)

# Plotting spring

# Simulate for different parameters
q, p = leap_frog_spring(0, 1, 0.1, 100)
axs[0].scatter(q, p, 3)

q, p = leap_frog_spring(1, 1, 0.1, 100)
axs[0].scatter(q, p, 3)

q, p = leap_frog_spring(0, 0.75, 0.1, 100)
axs[0].scatter(q, p, 3)

q, p = leap_frog_spring(0.25, 0.25, 0.1, 100)
axs[0].scatter(q, p, 3)

axs[0].set_box_aspect(1)
axs[0].set_title("Spring motion")
axs[0].set_xlabel('q')
axs[0].set_ylabel('p')
axs[0].legend(['q_0 = 0., p_0 = 1', 'q_0 = 1., p_0 = 1', 'q_0 = 0., p_0 = 0.75', 'q_0 = 0.25, p_0 = 0.25'], loc=1)

# Plotting pendulum

# Simulate for different parameters
q, p = leap_frog_pendulum(0.5, 0, 0.1, 500, 0.5)
axs[1].scatter(q, p, 3)

q, p = leap_frog_pendulum(1, 0, 0.1, 500, 0.5)
axs[1].scatter(q, p, 3)

q, p = leap_frog_pendulum(2, 0, 0.1, 500, 0.5)
axs[1].scatter(q, p, 3)

q, p = leap_frog_pendulum(3, 0, 0.1, 500, 0.5)
axs[1].scatter(q, p, 3)

# QUESTION:
# Why do I get these weird results for big initial q's? is that numerical instability?
# Uncomment those lines to plot
#q, p = leap_frog_pendulum(4, 0, 0.1, 500, 0.5)
#axs[1].scatter(q, p, 3)

axs[1].set_box_aspect(1)
axs[1].set_title("Pendulum motion, epsilon = 0.5, p_0 = 0")
axs[1].set_xlabel('q')
axs[1].legend(['q_0 = 0.5', 'q_0 = 1', 'q_0 = 2', 'q_0 = 3'], loc=1)
axs[1].set_ylim(-3, 3)


plt.show()