import matplotlib.pyplot as plt
from random import randint
from sys import argv
from rungekutta import rungekutta_main

plt.quiver(0, 0, 10, 10, headaxislength=3, headlength=3.5,
                color="black", angles="xy", scale_units="xy", scale=0.2)

plt.grid()
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()