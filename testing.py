import matplotlib.pyplot as plt
from random import randint
from sys import argv
from rungekutta import rungekutta_main

fig, axs = plt.subplots(2, 2)

X, Y, U = rungekutta_main()
for i, ax in enumerate(axs[0]):
    ax.plot(X, Y)
    ax.set_title(f"Static graph {i+1}")

# HODOGRAPH
frame_num = 1000
pause_length = 0.01
X_origins = X[::round(len(X) / frame_num)]
Y_origins = Y[::round(len(Y) / frame_num)]

for i in range(frame_num):
    for j, ax in enumerate(axs[1]):
        ax.clear()
        ax.set_title(f"Hodograph {j+1}")
        ax.plot(X, Y, color="tab:red")
        ax.quiver(X_origins[i], Y_origins[i], randint(80, 100), randint(80, 100),headaxislength=3, headlength=3.5,
                        color="red", angles="xy", scale_units="xy", scale=1)
    plt.pause(pause_length)

plt.show()
