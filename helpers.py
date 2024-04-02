"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose
from random import randint
import matplotlib.pyplot as plt

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# y(x) plot features
def create_plot(type, X, Y, y_slopes=None, hodograph=False, frames=0, pause=0):

    fig, ax = plt.subplots(1, 1)

    if hodograph:
        create_hodograph(X, Y, y_slopes, ax, frames, pause)
    else:
        if type == "RK4":
            plt.plot(X, Y, lw=3, color="tab:red")
            plt.title("Runge-Kutta 4 y(x) curve")
        elif type == "simulated":
            plt.plot(X, Y, lw=3, color="tab:blue")
            plt.title("Simulated y(x) curve from kinematic equations")

        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_ylim(0, y0+1)
        ax.set_xlim(0, xAxis(X, Y))
        ax.grid("both")
        plt.show()


# hodograph
def create_hodograph(X, Y, U, ax, frame_num, pause_length):

    X_origins = X[::round(len(X) / frame_num)]
    Y_origins = Y[::round(len(Y) / frame_num)]

    """
    Map X-origins to U(x) values. This approach may work because the x and y components of jerk depend on the slope of y(x) at each X_i value.
    Depending on frame_num, different X values will be used as origin, so it's better to map all the existing X values to U values
    for safety.
    """
    
    for i in range(frame_num):
        ax.clear()
        create_plot("RK4", X, Y, ax) # you gotta replot X and Y values in every frame
        ax.quiver(X_origins[i], Y_origins[i], randint(5, 10), randint(5, 10), 
                   angles="xy", scale_units="xy", scale=1)
        plt.pause(1)


# right-hand side of the autonomous differential equation for y''(x) = U'(x)
def Uprime(u, y_i):

    factor1 = Jf * (1 + pow(u, 2)) / (2 * pow(veloc(u, y_i), 2))
    radicand = pow(g/Q, 2) - (Jf * 4 * veloc(u, y_i) * Jt * (1 + pow(u, 2)))
    factor2 = (-1 * g/Q) + sqrt(radicand)
    return factor1 * factor2


# Velocity as a function of y
def veloc(u, y_i):
    second_term = 2 * g * (y0 - (y_i +(u*h))) / Q
    return sqrt(pow(v0, 2) + second_term)


# adaptive x-axis for better plot style
def xAxis(X, Y):
    
    # Find x-intercept
    for index in range(len(Y)):
        if isclose(Y[index], 0, abs_tol=0.1):
            Xintercept = X[index]
    try:
        return round(Xintercept)
    except:

        # return this if no Y value is near 0
        return xmax + 1


