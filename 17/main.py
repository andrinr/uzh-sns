from sph import SPH
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sph = SPH(1 << 8, 1)

fig, axs = plt.subplots(1)

scatter = axs.scatter(sph.pos[:,0], sph.pos[:,1])

def update(time):
    global sph, scatter
    sph.update()
    scatter.set_offsets(sph.pos)
    print(time)

animation = FuncAnimation(fig, update, frames=range(100), interval=10, repeat=False)

plt.show()