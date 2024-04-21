"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose
from scipy.optimize import curve_fit
from string import ascii_lowercase as alph
import time
import numpy as np
import matplotlib.pyplot as plt
import model_funcs as mf # type: ignore
import components as com # type: ignore
import computations as compute # type: ignore

# factor to scale up vectors in hodograph
vector_scale = 10

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()


# y(x) plot features
def create_plot(type, ax, data=[], div=(False, ())):

    # set features and plot X, Y values
    if type == "RK4":
        plt.plot(data[0], data[1], lw=2, color="tab:red", zorder=2)
        plt.title("Runge-Kutta 4 y(x) curve")
        if div[0]: 
            ax.scatter([div[1][0]], [div[1][1]], marker="x", s=30, color="black", zorder=3)
    elif type == "simulated":
        plt.plot(data[0], data[1], lw=2, color="tab:blue", zorder=2)
        plt.title("Simulated y(x) curve from kinematic equations")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_ylim(0, y0+(round(y0/8)))
    ax.set_xlim(0, xAxis(data[0], data[1]))
    ax.grid("both")


def set_view(ax, bounds=[]):
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def create_fit_curve(X, Y, model, initial_guess, x1, x2):
    start = time.time()

    popt, pcov = curve_fit(mf.models[model], X, Y, p0=initial_guess)
    X_reg = np.linspace(x1, x2, 10000)
    Y_reg = mf.models[model](X_reg, *popt)

    plt.plot(X_reg, Y_reg, "--", color="black", label="Best-fit curve", zorder=1)
    print(f"Curve-fitting execution time: {round(time.time() - start, 2)} seconds")
    print_popt(model, *popt)


def create_parabolic_fall(ax, X, Y):
    ax.plot(X, Y, ".", color="gray", label="Parabolic free fall", zorder=1)


# hodograph
def create_hodograph(type, hodo_type, ax, X, Y, U=[], frame_num=100, pause_length=0.1, div=(False, ())):

    # Create one origin (x, y) for the vector in each frame
    X_origins = X[::round(len(X) / frame_num)]
    Y_origins = Y[::round(len(Y) / frame_num)]
    U_origins = U[::round(len(X) / frame_num)]

    vector = hodo_type.split("_")
    x_comp_funcs = {"jerk": com.jerk_xcomp, "accel": com.accel_xcomp}
    y_comp_funcs = {"jerk": com.jerk_ycomp, "accel": com.accel_ycomp}

    for i in range(frame_num):
        ax.clear()
        create_plot(type, ax, X, Y) 
        if div[0]: 
            ax.scatter([div[1][0]], [div[1][1]], marker="x", s=30, color="black", zorder=3)
        if Y_origins[i] > 0:

            # compute x and y components to plot total vector
            x_comp = vector_scale * x_comp_funcs[vector[0]](U_origins[i], Y_origins[i])
            y_comp = vector_scale * y_comp_funcs[vector[0]](U_origins[i], Y_origins[i])
            ax.quiver(X_origins[i], Y_origins[i], x_comp, y_comp, headaxislength=3, headlength=3.5,
                    color="red", angles="xy", scale_units="xy", scale=1)
            
            # Plot additional components if requested
            if hodo_type != "jerk" or hodo_type != "accel":
                hodograph_components(vector, ax, X_origins[i], Y_origins[i], U_origins[i], x_comp, y_comp)
                
        else: break
        plt.pause(pause_length)
    plt.show()


def divergence_point(ax, X, Y, U):

    # find (X_i, Y_i) where normal acceleration due to gravity is less than the radial acceleration of the curvature
    print()
    for i in range(len(X)):
        veloc = compute.speed(U[i], Y[i])
        radial_accel = pow(veloc, 2) * (compute.Uprime(U[i], Y[i]) / pow(sqrt(1 + pow(U[i], 2)), 3))
        normal_gravity_accel = g / sqrt(1 + pow(U[i], 2))

        if Jt > 0: radial_accel = abs(radial_accel) # DOUBLE CHECK THE LOGIC OF THESE SIGNS
        elif Jt < 0 and radial_accel < 0: radial_accel = -1 * radial_accel

        if radial_accel > normal_gravity_accel:
            print_divPoint(X[i], Y[i], radial_accel, normal_gravity_accel, veloc)
            if dt != 0: 
                X_parabolic, Y_parabolic = compute.parabolic_free_fall((X[i], Y[i]), veloc, U[i], 1000)
                ax.plot(X_parabolic, Y_parabolic, linestyle="dotted", color="gray", label="Parabolic free fall", zorder=1)
            return X[i], Y[i]
        
    print("No divergence point exists.")
    print()
    return None, None


def hodograph_components(vector, ax, X_origin, Y_origin, u, x_comp, y_comp):

    # map user input to component functions
    tan_comp_funcs = {"jerk": com.tangential_jerk, "accel": com.tangential_accel}
    norm_comp_funcs = {"jerk": com.normal_jerk, "accel": com.normal_accel}

    # if vector = ["jerk", "comp"]
    if len(vector) == 2:
        ax.quiver(X_origin, Y_origin, x_comp, 0, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, 0, y_comp, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        
    # if vector = ["jerk", "tan", "norm"]
    elif len(vector) == 3:

        # compute normal and tangent vectors in terms of x and y components
        x_tan, y_tan = tan_comp_funcs[vector[0]](u, Y_origin)[0]
        x_norm, y_norm = norm_comp_funcs[vector[0]](u, Y_origin)[0]

        # plot normal and tangent vectors
        ax.quiver(X_origin, Y_origin, vector_scale * x_tan, vector_scale * y_tan, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)
        ax.quiver(X_origin, Y_origin, vector_scale * x_norm, vector_scale * y_norm, headaxislength=2, headlength=2, 
                  angles="xy", scale_units="xy", scale=1)


def print_divPoint(x, y, radial_accel, normal_gravity_accel, veloc):
    print(f"Divergence point: (x, y) = ({x}, {y})")
    print(f"Radial accel. due to curvature: {radial_accel} m/s^2")
    print(f"Normal accel. due to gravity: {normal_gravity_accel} m/s^2")
    print(f"Speed: {veloc} m/s")
    print()


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


# adaptive x-axis
def xAxis(X, Y):
    
    # Find x-intercept
    for index in range(len(Y)):
        if isclose(Y[index], 0, abs_tol=0.1):
            Xintercept = X[index]
    try:
        return round(Xintercept)
    except:
        return xmax + 1

