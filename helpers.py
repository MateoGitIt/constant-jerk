"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose
from random import uniform
import matplotlib.pyplot as plt

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()


def accel_xcomp(test):
    return test


def accel_ycomp(test):
    return test


def accel_tancomp(test):
    return test, test


def accel_normcomp(test):
    return test, test


# y(x) plot features
def create_plot(type, ax, X, Y, view=False, bounds=[]):

    # set features and plot X, Y values
    if type == "RK4":
        plt.plot(X, Y, lw=2, color="tab:red")
        plt.title("Runge-Kutta 4 y(x) curve")
    elif type == "simulated":
        plt.plot(X, Y, lw=2, color="tab:blue")
        plt.title("Simulated y(x) curve from kinematic equations")

    if view: 
        ax.set_xlim(bounds[0], bounds[1])
        ax.set_ylim(bounds[2], bounds[3])
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    else:
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_ylim(0, y0+1)
        ax.set_xlim(0, xAxis(X, Y))
    ax.grid("both")


# hodograph
def create_hodograph(type, hodo_type, ax, X, Y, y_slopes=None, frame_num=100, pause_length=0.1):

    # Create one origin (x, y) for the vector in each frame
    X_origins = X[::round(len(X) / frame_num)]
    Y_origins = Y[::round(len(Y) / frame_num)]

    """
    For better design, the functions for the x, y, tangent, and normal components of different vectors are mapped to different inputs the user may
    provide. To call these functions, the user's input is used as the dictionary's key. 
    """

    vector = hodo_type.split("_")
    x_comp_funcs = {"jerk": jerk_xcomp, "accel": accel_xcomp}
    y_comp_funcs = {"jerk": jerk_ycomp, "accel": accel_ycomp}

    for i in range(frame_num):
        ax.clear()
        create_plot(type, ax, X, Y) 
        if Y_origins[i] > 0:

            # compute x and y components to plot total vector
            x_comp = x_comp_funcs[vector[0]](uniform(0, 0.5))
            y_comp = y_comp_funcs[vector[0]](uniform(0, 0.5))
            ax.quiver(X_origins[i], Y_origins[i], x_comp, y_comp, headaxislength=3, headlength=3.5,
                    color="red", angles="xy", scale_units="xy", scale=1)
            
            # Plot additional components if requested
            if hodo_type != "jerk" or hodo_type != "accel":
                hodograph_components(vector, ax, X_origins[i], Y_origins[i], x_comp, y_comp)
                
        else: break
        plt.pause(pause_length)
    plt.show()


def hodograph_components(vector, ax, X_origin, Y_origin, x_comp, y_comp):

    # map user input to component functions
    tan_comp_funcs = {"jerk": jerk_tancomp, "accel": accel_tancomp}
    norm_comp_funcs = {"jerk": jerk_normcomp, "accel": accel_normcomp}

    # if vector = ["jerk", "comp"]
    if len(vector) == 2:
        ax.quiver(X_origin, Y_origin, x_comp, 0, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, 0, y_comp, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        
    # if vector = ["jerk", "tan", "norm"]
    elif len(vector) == 3:

        # compute normal and tangent vectors in terms of x and y components
        x_tan, y_tan = tan_comp_funcs[vector[0]](uniform(0, 0.5))
        x_norm, y_norm = norm_comp_funcs[vector[0]](uniform(0, 0.5))

        # plot normal and tangent vectors
        ax.quiver(X_origin, Y_origin, x_tan, y_tan, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, x_norm, y_norm, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)


# verify inputs for hodograph
def hodograph_inputs(frame_num, pause_length):

    if type(int(frame_num)) != int:
        exit("Number of frames (third CLA) must be an integer value.")
    if type(float(pause_length)) != float or float(pause_length) >= 1:
        exit("Pause length (fourth CLA) must be floating-point value less than 1.")
    
    return int(frame_num), float(pause_length)


def jerk_xcomp(test):
    return test


def jerk_ycomp(test):
    return test


def jerk_tancomp(test):
    return test, test

def jerk_normcomp(test):
    return test, test

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


