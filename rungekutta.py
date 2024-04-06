from inputParams import parameters
from math import pow, sqrt
from sys import exit, argv
from helpers import create_plot, create_hodograph, Uprime, hodograph_inputs
import time
import matplotlib.pyplot as plt
import numpy as np

"""

COMMAND-LINE USE: python rungekutta.py [vector] [frame number] [pause length]

"""

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare array for U_i, Y_i, and x_i values
U = []
Y = []
X = np.linspace(0, xmax, int(xmax / h)) 
X = X.tolist()

# macroscopic view option
view = False
bounds = []
if len(argv) == 3 and argv[1] == "view":
    view = True
    bounds = argv[2].split(",")
    bounds = [int(x) for x in bounds]

# hodograph inputs
hodo = False
frame_num = -1
pause_length = -1

if len(argv) == 4 and (argv[1] in ["jerk", "accel"] or argv[1] in ["jerk_comp", "jerk_tan_norm", "accel_comp", "accel_tan_norm"]):
    hodo = True
    frame_num, pause_length = hodograph_inputs(argv[2], argv[3])

# append initial height
Y.append(y0)

# calculate U0 (which equals y'(x) at t = 0) and append to U array
try:
    U0 = -1 * (a0/g) / sqrt(1 - pow(a0/g, 2))
except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
U.append(U0)

def main():

    # calculate new U and Y values and record them in lists
    for i in range(1, len(X)):
        k1, k2, k3, k4 = rungekutta_kvalues(U[i-1], Y[i-1])
        new_U = U[i-1] + (h/6)*(k1 + (2*k2) + (2*k3) + k4)
        U.append(new_U)
        new_Y = Y[i-1] + (U[i-1] * h)
        Y.append(new_Y)

    return X, Y, U


def rungekutta_kvalues(u, y_i):
    k1 = Uprime(u, y_i)
    k2 = Uprime(u + (h * (k1/2)), y_i)
    k3 = Uprime(u + (h * (k2/2)), y_i)
    k4 = Uprime(u + (h * k3), y_i)
    return k1, k2, k3, k4


if __name__ == "__main__":
    start =  time.time()
    try:
        main()
    except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
        
    print(f"RK4 execution time: {round(time.time() - start, 2)} seconds")

    # create plot
    fig, ax = plt.subplots(1, 1)
    if hodo: 
        fig.canvas.mpl_connect("close_event", exit)
        create_hodograph("RK4", argv[1], ax, X, Y, frame_num=frame_num, pause_length=pause_length)
    else: 
        create_plot("RK4", ax, X, Y, view=view, bounds=bounds)
        plt.show()
