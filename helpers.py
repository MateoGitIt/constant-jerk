"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose
from random import uniform
from scipy.optimize import curve_fit
from string import ascii_lowercase as alph
import time
import model_funcs as mf
import numpy as np
import components as com # type: ignore
import matplotlib.pyplot as plt


# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()


# available model functions for curve fitting. Add a new model function here.
model_funcs = ["parabola"]


# y(x) plot features
def create_plot(type, ax, X, Y, view=False, bounds=[]):

    # set features and plot X, Y values
    if type == "RK4":
        plt.plot(X, Y, lw=2, color="tab:red", zorder=2)
        plt.title("Runge-Kutta 4 y(x) curve")
    elif type == "simulated":
        plt.plot(X, Y, lw=2, color="tab:blue", zorder=2)
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
        ax.set_ylim(0, y0+(round(y0/8)))
        ax.set_xlim(0, xAxis(X, Y))
    ax.grid("both")


def create_fit_curve(X, Y, model, initial_guess, x1, x2):
    
    start = time.time()
    popt, pcov = curve_fit(mf.models[model], X, Y, p0=initial_guess)
    X_reg = np.linspace(x1, x2, 100)
    Y_reg = mf.models[model](X_reg, *popt)
    plt.plot(X_reg, Y_reg, "--", color="black", label="Best-fit curve", zorder=1)
    print(f"Curve-fitting execution time: {round(time.time() - start, 2)} seconds")
    print_popt(model, *popt)


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
    x_comp_funcs = {"jerk": com.jerk_xcomp, "accel": com.accel_xcomp}
    y_comp_funcs = {"jerk": com.jerk_ycomp, "accel": com.accel_ycomp}

    for i in range(frame_num):
        ax.clear()
        create_plot(type, ax, X, Y) 
        if Y_origins[i] > 0:

            # compute x and y components to plot total vector
            x_comp = x_comp_funcs[vector[0]](uniform(8, 11))
            y_comp = y_comp_funcs[vector[0]](uniform(8, 11))
            ax.quiver(X_origins[i], Y_origins[i], x_comp, y_comp, headaxislength=3, headlength=3.5,
                    color="red", angles="xy", scale_units="xy", scale=1)
            
            # Plot additional components if requested
            if hodo_type != "jerk" or hodo_type != "accel":
                hodograph_components(vector, ax, X_origins[i], Y_origins[i], x_comp, y_comp)
                
        else: break
        plt.pause(pause_length)
    plt.show()


def curve_fit_inputs(model, params):

    params = [float(x) for x in params.split(",")]
    if len(model.split("_")) == 2 and model.split("_")[1] == "poly":
        deg = int(model.split("_")[0])
        if deg > 10: 
            exit(f"A {deg}-degree polynomial model is not available. You must implement it in the source code.")
        if len(params) - 1 != deg:
            exit(f"This polynomial takes in {deg+1} parameters, not {len(params)}.")
    elif model == "line" and len(params) != 2:
        exit(f"The linear model only accepts 2 initial parameters, not {len(params)}.")
    elif model == "ellipse" and len(params) != 4:
        exit(f"The elliptical model only accepts 4 parameters, not {len(params)}.")
    elif model == "exponential" and len(params) != 4:
        exit(f"The exponential model only accepts 4 parameters, not {len(params)}.")

    return True

def hodograph_components(vector, ax, X_origin, Y_origin, x_comp, y_comp):

    # map user input to component functions
    tan_comp_funcs = {"jerk": com.jerk_tancomp, "accel": com.accel_tancomp}
    norm_comp_funcs = {"jerk": com.jerk_normcomp, "accel": com.accel_normcomp}

    # if vector = ["jerk", "comp"]
    if len(vector) == 2:
        ax.quiver(X_origin, Y_origin, x_comp, 0, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, 0, y_comp, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        
    # if vector = ["jerk", "tan", "norm"]
    elif len(vector) == 3:

        # compute normal and tangent vectors in terms of x and y components
        x_tan, y_tan = tan_comp_funcs[vector[0]](uniform(8, 11))
        x_norm, y_norm = norm_comp_funcs[vector[0]](uniform(8, 11))

        # plot normal and tangent vectors
        ax.quiver(X_origin, Y_origin, x_tan, y_tan, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, x_norm, y_norm, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)


# verify inputs for hodograph
def hodograph_inputs(argv):

    if argv[1] not in ["jerk", "jerk_comp", "jerk_tan_norm", "accel", "accel_comp", "accel_tan_norm"]:
        exit("To display a hodograph, you must select one of the following as the second CLA: " 
             "'jerk', 'jerk_comp', 'jerk_tan_norm', 'accel', 'accel_comp', or 'accel_tan_norm'. ")
    try:
        int(argv[2])
        float(argv[3])
    except:
        exit("One of your inputs for the number of frames or pause length is invalid.")
    
    if float(argv[3]) >= 1:
            exit("Pause length (fourth CLA) must be floating-point value less than 1.")

    return True, int(argv[2]), float(argv[3])


def print_popt(model, *params):
    params = [x for x in params]
    print("__________________________________\n")

    if len(model.split("_")) == 2 and model.split("_")[1] == "poly":
        if model.split("_")[1] == "poly":
            model_tag = f"{model.split('_')[0]}-degree polynomial"
    elif model == "line":
        model_tag = "y = ax + b line"
    elif model == "ellipse":
        model_tag = "ellipse of the form y = b * sqrt(1-[(x-c)/a]^2) + d centered at (c, d)"
    elif model == "exponential":
        model_tag = "exponential of the form y = a * e^(bx) + c"

    print(f"Coefficients of best-fit {model_tag} are:\n")
    for i, coef in enumerate(params):
        print(f"{alph[i]}: {coef}")        
        
    print("\n__________________________________\n")


# 1) Implement vector functions for hodograph
# 3) Point where object diverges from the curve and follows parabolic motion


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


def view_inputs(argv):

    if len(argv) == 5: bounds = argv[4].split(",")
    elif len(argv) == 3: bounds = argv[2].split(",")
    bounds = [int(x) for x in bounds]
    if bounds[0] < bounds[1] and bounds[2] < bounds[3]:
        return bounds, True
    else:
        exit("Bounds are incorrect. Accepted format is x1,x2,y1,y2 where x1 and y1 must "
             "be less than x2 and y2, respectively.")


# adaptive x-axis for better plot style
def xAxis(X, Y):
    
    # Find x-intercept
    for index in range(len(Y)):
        if isclose(Y[index], 0, abs_tol=0.1):
            Xintercept = X[index]
    try:
        return round(Xintercept)
    except:
        return xmax + 1

