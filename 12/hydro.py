import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Init vars, data
N = 100
delta_x = 1
gamma = 3

# Initialize shock tube
U_shock = np.zeros((3, N))
e = 10**-5
# p = 1
U_shock[0] = 1
# p = 4
U_shock[0, int(N / 1.5):N] = 4
# u = 0 => pu = 0
U_shock[1] = 0

# E = 0.5 * p*u^2 + p*e
# u = 0 => E = p*e
U_shock[2] = U_shock[0] * e


# Initialize blast wave
U_blast = np.zeros((3, N))
e = 10**-5
# p = 1
U_blast[0] = 1
# pu = 0
U_blast[1] = 0

# E = 0.5 * p*u^2 + p*e
# u = 0 => E = p*e
U_blast[2] = U_blast[0] * e

# Point explosion
# p = 1, e = 1 => 1 * 1 => 1
U_blast[2, int(N/3)] = 1


def forces(U):
    # U spatial Left and right
    U_l = np.roll(U, 1, 1)
    U_r = np.roll(U, -1, 1)

    # Density
    p = U[0]

    # Mass
    pu = U[1]

    # Velocity in x dir
    u = pu / p
    u_l = np.roll(u, 1)
    u_r = np.roll(u, -1)

    # Energy
    E = U[2]

    # p*u^2
    pu_sq = pu * u

    # Calculate pressure
    P = 2 * E - pu_sq

    # Speed of sound
    # dependant on pressure and degrees of freedom of gas
    if (min(P) < 0):
        print("neg P")

    c = np.sqrt(P / p * gamma)
    c_l = np.roll(c, 1)
    c_r = np.roll(c, -1)

    # Calculate force
    F = np.array([
        pu, 2 * E, u * (E + P)
    ])

    # Force spatial left and right
    F_r = np.roll(F, -1, 1)
    F_l = np.roll(F, 1, 1)

    # Force spatial left and right, half steps
    D_max_l = np.maximum(np.absolute(u_l) + c_l, np.absolute(u) + c)
    F_hl = 0.5 * (F + F_l) - 0.5 * D_max_l * (U - U_l)
    D_max_r = np.maximum(np.absolute(u_r) + c_r, np.absolute(u) + c)
    F_hr = 0.5 * (F + F_r) - 0.5 * D_max_r * (U - U_r)

    # Dynamicly calculate t
    delta_t = 0.1 * delta_x/max(np.absolute(u) + c)

    return F_l, F_r, F_hl, F_hr, U_l, U_r, delta_t


class Hydro:
    def __init__(self, U, method):
        self.U = U
        self.method = method

    def step(self):

        # Calculate forces
        F_l, F_r, F_hl, F_hr, U_l, U_r, delta_t = forces(self.U)

        print(delta_t)

        # LAX method
        if self.method == 'A':
            self.U = 0.5 * (U_r + U_l) - delta_t / (2.*delta_x) * (F_r + F_l)

        # Riemann solver
        if self.method == 'B':
            self.U = self.U - delta_t / delta_x * (F_hr - F_hl)

        # Riemann solver with half time steps
        # actual name is Rusanov or Local-Lax Friedrich scheme?
        if self.method == 'C':
            # Estimate U at half time step
            U_ht = self.U - 0.5 * delta_t / delta_x * (F_hr - F_hl)

            # Calculate force at half spatial/time step
            F_l_ht, F_r_ht, F_hl_ht, F_hr_ht, U_l_ht, U_r_ht, delta_t = forces(U_ht)

            self.U = self.U - delta_t / delta_x * (F_hr_ht - F_hl_ht)

        #print(self.method, self.U)

hydros = [
    Hydro(U_shock, 'A'),
    Hydro(U_shock, 'B'),
    Hydro(U_shock, 'C'),
    Hydro(U_blast, 'A'),
    Hydro(U_blast, 'B'),
    Hydro(U_blast, 'C')
]

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 2)
x = np.linspace(0, N, N)

titles = [
    "Method A, Shock tube",
    "Method B, Shock tube",
    "Method C, Shock tube",
    "Method A, Blast wave",
    "Method B, Blast wave",
    "Method C, Blast wave",
]

axes = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[1, 0]),
    fig.add_subplot(gs[2, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[1, 1]),
    fig.add_subplot(gs[2, 1])
]

lineplots = []

for i in range(6):
    axes[i].set_ylim(-1, 4.5)
    axes[i].set_title(titles[i])
    for j in range(3):
        lineplots.append(axes[i].plot(x, hydros[i].U[j])[0])


def update(i):
    for substeps in range(1):
        for k in range(6):
            hydros[k].step()
            for j in range(3):
                lineplots[k*3+j].set_data(x, hydros[k].U[j])


ani = FuncAnimation(fig, update, 1000, interval=20, repeat=False)

plt.show()