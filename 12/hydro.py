import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Init vars, data
N = 1000
delta_x = 0.1
delta_t = 0.001

U_A = np.ones((3, N))
U_B = np.ones((3, N))
U_C = np.ones((3, N))


def forces(U):

    # U spatial Left and right
    U_r = np.roll(U, -1, 1)
    U_l = np.roll(U, 1, 1)

    # Density
    p = U[0]

    # Mass
    pu = U[1]

    # Velocity
    u = pu / p
    u_l = np.roll(u, 1)
    u_r = np.roll(u, -1)

    # Energy
    E = U[2]

    # p*u^2
    pu_sq = p * u ** 2

    # Calculate pressure
    P = 2 * E - pu_sq

    # Speed of sound
    # dependant on pressure and degrees of freedom of gas
    c = np.sqrt(P / p * 3)

    # Calculate force
    F = np.array([
        pu, 2 * E, pu / p * (0.5 * pu_sq + 3 / 2 * P)
    ])

    # Force spatial left and right
    F_r = np.roll(F, -1, 1)
    F_l = np.roll(F, 1, 1)

    # Force spatial left and right, half steps
    F_hl = 0.5 * (F + F_l) - 0.5 * np.maximum(
        np.absolute(u_l) + c, np.absolute(u) + c
    ) * (U - U_l)
    F_hr = 0.5 * (F + F_r) - 0.5 * np.maximum(
        np.absolute(u_r) + c, np.absolute(u) + c
    ) * (U - U_r)

    return F_hl, F_hr, U_l, U_r


# Forces at i +/- 0.5
def step(U, method):

    F_hl, F_hr, U_l, U_r = forces(U)

    # Different methods
    # No half time steps
    if method == 'A':
        return 0.5 * (U_r + U_l) - delta_t / (0.5*delta_x) * (F_hr + F_hl)

    if method == 'B':
        return U - delta_t / delta_x * (F_hr - F_hl)

    # With time half steps
    if method == 'C':
        # Estimate U at half time step
        U_ht = U - delta_t / (0.5*delta_x) * (F_hr - F_hl)

        # Calculate force half step time and spatial
        F_hl_ht, F_hr_ht, U_l_ht, U_r_ht = forces(U_ht)

        return U - delta_x / delta_x * (F_hr_ht - F_hl_ht)


iterations = 100
for i in range(iterations):
    U_A = step(U_A, 'A')
    U_B = step(U_B, 'B')
    U_C = step(U_C, 'C')

plt.plot(U_A[0])

plt.show()