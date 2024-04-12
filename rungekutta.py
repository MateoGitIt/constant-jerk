from inputParams import parameters
from math import pow, sqrt
from sys import exit, argv
from model_funcs import models # type: ignore
from computations import Uprime # type: ignore
import helpers as hel
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

# INPUT: macroscopic view option
view = False
bounds = []
if len(argv) == 3 and argv[1] == "view":
    bounds, view = hel.view_inputs(argv)

# INPUT: best fit curve
best_curve = False
if (len(argv) == 3 or len(argv) == 5) and argv[1] in models:
    best_curve = hel.curve_fit_inputs(argv[1], argv[2])
    if len(argv) == 5 and argv[3] == "view":
        bounds, view = hel.view_inputs(argv)

# INPUT: hodograph
hodo = False
if len(argv) == 4:
    hodo, frame_num, pause_length = hel.hodograph_inputs(argv)

# append initial height
Y.append(y0)

# calculate U0 (which equals y'(x) at t = 0) and append to U array
try:
    U0 = -1 * (a0/g) / sqrt(1 - pow(a0/g, 2))
except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
U.append(U0)

def rungekutta_main():

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
        X, Y, U = rungekutta_main()
    except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
        
    print(f"RK4 execution time: {round(time.time() - start, 2)} seconds")

    # divergence point between curve and object's trajectory
    show_div = False
    divPoint = hel.divergence_point(X, Y, U)
    if divPoint != (None, None): show_div = True

    # create plot
    fig, ax = plt.subplots(1, 1)
    if hodo: 
        fig.canvas.mpl_connect("close_event", exit)
        hel.create_hodograph("RK4", argv[1], ax, X, Y, frame_num=frame_num, pause_length=pause_length, div=(show_div, divPoint))
    else: 
        hel.create_plot("RK4", ax, X, Y, view=view, bounds=bounds, div=(show_div, divPoint))
        if best_curve: 
            initial_guess = [float(x) for x in argv[2].split(",")]
            if len(bounds) == 4: 
                hel.create_fit_curve(X, Y, argv[1], initial_guess, bounds[0], bounds[1])
            else: 
                hel.create_fit_curve(X, Y, argv[1], initial_guess, -(xmax+round(0.15*xmax)), xmax + round(0.15*xmax))
        plt.show()
