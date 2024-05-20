"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose
from scipy.optimize import curve_fit
from string import ascii_lowercase as alph
from sklearn.metrics import r2_score
import sigfig as sf
import time
import numpy as np
import matplotlib.pyplot as plt
import model_funcs as mf # type: ignore
import components as com # type: ignore
import computations as compute # type: ignore

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()


# y(x) plot features
def create_plot(type, ax, data=[], div=(False, 0, 0, 0, 0)):

    # set features and plot X, Y values
    if type == "rk4":
        ax.plot(data[0], data[1], lw=2, color="tab:red", zorder=2)
        ax.set_title("Runge-Kutta 4 y(x) curve")
        if div[0]: 
            X_parabolic, Y_parabolic = compute.parabolic_free_fall((div[1], div[2]), div[3], div[4], 1000)
            plot_divergent_free_fall(ax, div[1], div[2], X_parabolic, Y_parabolic)
    elif type == "kinematics":
        ax.plot(data[0], data[1], lw=2, color="tab:blue", zorder=2)
        ax.set_title("Simulated y(x) curve from kinematic equations")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_ylim(0, y0+(round(y0/8)))
    ax.set_xlim(0, xAxis(data[0], data[1]))
    ax.grid("both")


def set_view(ax, bounds):
    # if called, this function overwrites the view set by create_plot
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def create_fit_curve(model, ax, initial_guess, x1, x2, data=[], curve_tag=""):

    start = time.time()
    popt, pcov = curve_fit(mf.models[model], data[0], data[1], p0=initial_guess)
    Y_reg = mf.models[model](np.array(data[0]), *popt)
    X_reg_left = np.linspace(x1, round(data[0][0]), 1000)
    X_reg_right = np.linspace(round(data[0][-1]), x2, 1000)

    label_text = f"{model} R^2={sf.round(r2_coefficient(Y_reg, data[1]), 5)}"
    line_color = ax._get_lines.get_next_color()
    ax.plot(data[0], Y_reg, "--", color=line_color, label=label_text, zorder=1)
    ax.plot(X_reg_left, mf.models[model](X_reg_left, *popt), "--", color=line_color, zorder=1)
    ax.plot(X_reg_right, mf.models[model](X_reg_right, *popt), "--", color=line_color, zorder=1)
    print(f"Curve-fitting execution time: {round(time.time() - start, 2)} seconds")
    print_popt(model, curve_tag, *popt)


# hodograph
def create_hodograph(type, hodo_type, ax, X, Y, U=[], frame_num=100, pause_length=0.1, 
                     div=(False, 0, 0, 0, 0), view=[], scale=1):
    
    # Create one origin (x, y) for the vector in each frame
    X_origins = X[::len(X) // frame_num]
    Y_origins = Y[::len(Y) // frame_num]
    U_origins = U[::len(X) // frame_num]
    vector_type, *comps = hodo_type.split("_")
    view_setting = True if len(view) > 0 else False
    divergence = div[0]
    comps_length = len(comps)

    # properties of the arrows displayed by ax.quiver()
    quiver_params = {
        "headaxislength": 3,
        "headlength": 3.5,
        "color": "black",
        "angles": "xy",
        "scale_units": "xy",
        "scale": 1/scale,
        "zorder": 3
    }

    # Compute vectors
    Xc, Yc = com.vector_xy(vector_type, frame_num, U_origins, Y_origins, X_origins)
    if comps_length == 2:
        tang, norm = com.vector_tang_norm(vector_type, frame_num, U_origins, Y_origins, X_origins)

    # Compute parabolic free fall trajectory
    div_x, div_y = (div[1], div[2])
    X_parabolic, Y_parabolic = compute.parabolic_free_fall((div_x, div_y), div[3], div[4], 1000)
    
    for i in range(frame_num):
        ax.clear()
        create_plot(type, ax, data=[X, Y])
        if view_setting: set_view(ax, view)
        if divergence: plot_divergent_free_fall(ax, div_x, div_y, X_parabolic, Y_parabolic)
        ax.quiver(X_origins[i], Y_origins[i], Xc[i], Yc[i], **quiver_params)
        if comps_length == 1:
            ax.quiver(X_origins[i], Y_origins[i], Xc[i], 0, **quiver_params)
            ax.quiver(X_origins[i], Y_origins[i], 0, Yc[i], **quiver_params)
        elif comps_length == 2:
            #print(f"tangential: ({tang[i, 0]}, {tang[i, 1]})")
            #print(f"normal: ({norm[i, 0]}, {norm[i, 1]})")
            ax.quiver(X_origins[i], Y_origins[i], tang[i, 0], tang[i, 1], **quiver_params)
            ax.quiver(X_origins[i], Y_origins[i], norm[i, 0], norm[i, 1], **quiver_params)
        plt.pause(pause_length)
    plt.show() # check if this plt.show() really goes here


def divergence_point(X, Y, U):

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
            return X[i], Y[i], U[i], veloc
        
    print("No divergence point exists in the given curve.")
    print()
    return None, None, None, None


def plot_divergent_free_fall(ax, x, y, X_parabolic, Y_parabolic):
    ax.scatter(x, y, marker="x", s=30, color="black", zorder=3)
    ax.plot(X_parabolic, Y_parabolic, linestyle="dotted", color="gray", label="Parabolic free fall", zorder=1)


def print_divPoint(x, y, radial_accel, normal_gravity_accel, veloc):
    print(f"Divergence point: (x, y) = ({x}, {y})")
    print(f"Radial accel. due to curvature: {radial_accel} m/s^2")
    print(f"Normal accel. due to gravity: {normal_gravity_accel} m/s^2")
    print(f"Speed: {veloc} m/s")
    print()


def print_popt(model, curve_tag, *params):
    params = [x for x in params]

    if len(model.split("_")) == 2 and model.split("_")[1] == "poly":
        if model.split("_")[1] == "poly":
            model_tag = f"{model.split('_')[0]}-degree polynomial"
    elif model == "line":
        model_tag = "y = ax + b line"
    elif model == "ellipse":
        model_tag = "ellipse of the form y = b * sqrt(1-[(x-c)/a]^2) + d centered at (c, d)"
    elif model == "exponential":
        model_tag = "exponential of the form y = a * e^(bx) + c"

    print(f"Coefficients of best-fit {model_tag} for {curve_tag} curve are:\n")
    for i, coef in enumerate(params):
        print(f"{alph[i]}: {coef}")        
        
    print("\n__________________________________\n")


def r2_coefficient(Y_pred, Y_true):
    return r2_score(Y_true, Y_pred)


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

