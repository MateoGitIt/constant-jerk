"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
from math import sqrt, pow, isclose, degrees
from scipy.optimize import curve_fit
from string import ascii_lowercase as alph
from sklearn.metrics import r2_score
import sigfig as sf
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.quiver as matquiver
import model_funcs as mf # type: ignore
import components as com # type: ignore
import computations as compute # type: ignore

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt, decs = parameters.values()
pause_state = False
final_frame = 0
pause_keys = ['p', '\b', 'enter', 'escape']


# y(x) plot features
def create_plot(type, ax, data=[], div=(False, 0, 0, 0, 0), view=(False, 0, 0, 0, 0), show_textbox=False):

    # set features and plot X, Y values
    if view[0]:
        view_setting, x1, x2, y1, y2 = view
    else:
        view_setting = False

    if type == "rk4":
        ax.plot(data[0], data[1], lw=2, label="y(x)", color="tab:red", zorder=2)
        ax.set_title("Runge-Kutta 4 y(x) curve")
        if div[0] and (div[1], div[2]) != (None, None): 
            X_parabolic, Y_parabolic = compute.parabolic_free_fall((div[1], div[2]), div[3], div[4], 1000)
            plot_divergent_free_fall(ax, div[1], div[2], X_parabolic, Y_parabolic)
    elif type == "kinematics":
        ax.plot(data[0], data[1], label="y(x)", lw=2, color="tab:blue", zorder=2)
        ax.set_title("Simulated y(x) curve from kinematic equations")

    if view_setting:
        set_view(ax, [x1, x2, y1, y2])
    else:
        ax.set_ylim(0, y0+(round(y0/8)))
        ax.set_xlim(0, xAxis(data[0], data[1]))
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid("both")

    if show_textbox: print_initial_conditions(ax)


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
def create_hodograph(type, vectors, ax, X, Y, U=[], frame_num=100, pause_length=0.1, 
                     div=(False, 0, 0, 0, 0), view=[], color_list=[]):
    
    # Create one origin (x, y) for the vector in each frame
    X_origins = X[::len(X) // frame_num]
    Y_origins = Y[::len(Y) // frame_num]
    U_origins = U[::len(X) // frame_num]

    xy_vectors, tang_norm_vectors, xy_scales, tang_norm_scales, total_scales, xy_colors, tang_norm_colors, total_colors = parse_vector_input(vectors, color_list)
    vectors_size = len(vectors)

    view_setting = True if len(view) > 0 else False
    divergence = True if div[0] and (div[1], div[2]) != (None, None) else False

    # properties of the arrows displayed by ax.quiver()
    quiver_params = {
        "headaxislength": 1,
        "headlength": 1.5,
        "width": 0.01,
        "angles": "xy",
        "scale_units": "xy",
        "zorder": 3
    }

    # Compute vectors
    X_components, Y_components, X_comp_additional, Y_comp_additional = [np.empty((vectors_size, frame_num)) for _ in range(4)]
    xy_vector_counter = 0
    vector_labels = []
    total_vectors = []
    for i, v in enumerate(vectors):
        vector_labels.append(f"{v[0]} (scale: {v[1]})")
        Xc, Yc = com.vector_xy(v[0], frame_num, U_origins, Y_origins, X_origins)
        X_components[i, :] = Xc
        Y_components[i, :] = Yc
        if v[0] in xy_vectors:
            X_comp_additional[xy_vector_counter] = X_components[i]
            Y_comp_additional[xy_vector_counter] = Y_components[i]
            xy_vector_counter += 1
        elif (v[0] not in xy_vectors) and (v[0] not in tang_norm_vectors):
            total_vectors.append(v[0])
    vector_labels = np.array(vector_labels)
    total_vectors = np.array(total_vectors)

    tang_norm_size = len(tang_norm_vectors)
    if tang_norm_size > 0:
        tang_components = np.empty((tang_norm_size, frame_num, 2))
        norm_components = np.empty((tang_norm_size, frame_num, 2))
        for i, vector in enumerate(tang_norm_vectors):
            tang, norm = com.vector_tang_norm(vector, frame_num, U_origins, Y_origins, X_origins)
            tang_components[i] = tang
            norm_components[i] = norm

    # Compute parabolic free fall trajectory
    div_x, div_y = (div[1], div[2])
    if divergence:
        X_parabolic, Y_parabolic = compute.parabolic_free_fall((div_x, div_y), div[3], div[4], 100)
    
    # Define ranges outside animation to decrease overhead of calling range()
    vector_seq = range(vectors_size)
    xy_seq = range(len(xy_vectors))
    tang_norm_seq = range(tang_norm_size)

    for i in range(frame_num):
        ax.clear()
        create_plot(type, ax, data=[X, Y])
        if view_setting: set_view(ax, view)
        if divergence: plot_divergent_free_fall(ax, div_x, div_y, X_parabolic, Y_parabolic)
        for j in vector_seq:
            ax.quiver(X_origins[i], Y_origins[i], X_components[j, i], Y_components[j, i], 
                      scale=1/total_scales[j], color=total_colors[j], label=vector_labels[j], **quiver_params)
        for j in xy_seq:
            ax.quiver(X_origins[i], Y_origins[i], X_comp_additional[j, i], 0, scale=1/xy_scales[j], color=xy_colors[j],
                      **quiver_params)
            ax.quiver(X_origins[i], Y_origins[i], 0, Y_comp_additional[j, i], scale=1/xy_scales[j], color=xy_colors[j],
                      **quiver_params)
        for j in tang_norm_seq:
            ax.quiver(X_origins[i], Y_origins[i], tang_components[j, i, 0], tang_components[j, i, 1], 
                      scale=1/tang_norm_scales[j], color=tang_norm_colors[j], **quiver_params)
            ax.quiver(X_origins[i], Y_origins[i], norm_components[j, i, 0], norm_components[j, i, 1], 
                      scale=1/tang_norm_scales[j], color=tang_norm_colors[j], **quiver_params)
        plt.legend()
        plt.pause(pause_length)
        if pause_state:
            print_final_hodo_state(frame_num, i, xy_vectors, tang_norm_vectors, total_vectors,
                                   X_origins, Y_origins, U_origins)
            create_plot(type, ax, data=[X, Y])
            if view_setting: set_view(ax, view)
            if divergence: plot_divergent_free_fall(ax, div_x, div_y, X_parabolic, Y_parabolic)
            plot_final_vectors(ax, quiver_params)
            plt.show()
            break


def pause_hodograph(event):
    if event.key in pause_keys:
        global pause_state
        pause_state = True


def print_final_hodo_state(frame_num, i, xy_vectors, tang_norm_vectors, total_vectors, X, Y, U):
    print(f"Paused at frame {i} out of {frame_num}")
    print(f"local angle: {round(degrees(compute.local_angle(U[i])), decs)}°\n")  
    for vector in total_vectors:
        if vector == "accel": print("Acceleration")
        else: print(vector.capitalize())
        x_comp, y_comp, magnitude = com.vector_xy_point(vector, i, X, Y, U)
        print(f"magnitude: {round(magnitude, decs)} {units(vector)}\n")

    for vector in xy_vectors:
        if vector == "accel": print("Acceleration")
        else: print(vector.capitalize())
        x_comp, y_comp, magnitude = com.vector_xy_point(vector, i, X, Y, U)
        print(f"x component: {round(x_comp, decs)} {units(vector)}")
        print(f"y component: {round(y_comp, decs)} {units(vector)}")
        print(f"magnitude: {round(magnitude, decs)} {units(vector)}\n")

    for vector in tang_norm_vectors:
        if vector == "accel": print("Acceleration")
        else: print(vector.capitalize())
        tang, norm, magnitude = com.vector_tang_norm_point(vector, i, X, Y, U)
        print(f"tangential: {round(tang, decs)} {units(vector)}")
        print(f"normal: {round(norm, decs)} {units(vector)}")
        print(f"magnitude: {round(magnitude, decs)} {units(vector)}\n")


def plot_final_vectors(ax, quiver_params):
    quiver_arrows = [child for child in ax.get_children() if isinstance(child, matquiver.Quiver)]
    for vector in quiver_arrows:
        ax.quiver(vector.X, vector.Y, vector.U, vector.V, scale=vector.scale, color=vector.get_facecolor()[0],
                  label=vector._label, **quiver_params)


def dot_product(v, w):
    return (v[0]*w[0]) + (v[1]*w[1])


def magnitude(v):
    return sqrt(pow(v[0], 2) + pow(v[1], 2))


def divergence_point(X, Y, U):

    # find (X_i, Y_i) where normal acceleration due to gravity is less than the radial acceleration of the curvature
    print()
    for i in range(len(X)):
        speed = compute.speed(U[i], Y[i])
        radial_accel = pow(speed, 2) * (compute.Uprime(U[i], Y[i]) / pow(sqrt(1 + pow(U[i], 2)), 3))
        normal_gravity_accel = g / sqrt(1 + pow(U[i], 2))

        if Jt > 0: radial_accel = abs(radial_accel) 
        elif Jt < 0 and radial_accel < 0: radial_accel = -1 * radial_accel

        if radial_accel > normal_gravity_accel:
            print_divPoint(round(X[i], decs), round(Y[i], decs), round(radial_accel, decs), round(normal_gravity_accel, decs), round(speed, decs))
            return X[i], Y[i], U[i], speed
        
    print("No divergence point exists in the given curve.")
    print()
    return None, None, None, None


def parse_vector_input(vectors, color_list):
    xy_vectors = []
    tang_norm_vectors = []
    xy_scales = {}
    tang_norm_scales = {}
    total_scales = {}
    total_colors = {}
    xy_colors = {}
    tang_norm_colors = {}
    for i, v in enumerate(vectors):
        total_colors[i] = color_list[i]
        total_scales[i] = v[1]
        if len(v) > 2:
            if v[2] == "xy":
                xy_vectors.append(v[0])
                xy_colors[len(xy_colors)] = color_list[i]
                xy_scales[len(xy_scales)] = v[1]
            elif v[2] == "tang_norm":
                tang_norm_vectors.append(v[0])
                tang_norm_colors[len(tang_norm_colors)] = color_list[i]
                tang_norm_scales[len(tang_norm_scales)] = v[1]
        elif len(v) == 1:
            exit("You must indicate at least a vector name and a scalar factor")
    return np.array(xy_vectors), np.array(tang_norm_vectors), xy_scales, tang_norm_scales, total_scales, xy_colors, tang_norm_colors, total_colors


def plot_divergent_free_fall(ax, x, y, X_parabolic, Y_parabolic):
    ax.scatter(x, y, marker="x", s=30, color="black", zorder=3)
    ax.plot(X_parabolic, Y_parabolic, linestyle="dotted", color="gray", label="Parabolic free fall", zorder=1)


def print_divPoint(x, y, radial_accel, normal_gravity_accel, speed):
    print(f"Divergence point: (x, y) = ({x}, {y})")
    print(f"radial accel. due to curvature: {radial_accel} m/s^2")
    print(f"normal accel. due to gravity: {normal_gravity_accel} m/s^2")
    print(f"speed: {speed} m/s")
    print()


def print_initial_conditions(ax):
    text = f"Height: {y0}m\nSpeed: {v0}m/s\nAccel: {a0}m/s2\nJerk:{Jt}m/s3"
    box = dict(boxstyle='round', fc='blanchedalmond', ec='orange', alpha=0.5, pad=0.5)
    x, y = (0.65 * ax.get_xlim()[1], 0.93 * ax.get_ylim()[0])
    if y == 0:
        y = 0.07 * ax.get_ylim()[1]
    ax.text(x, y, text, fontsize=10, bbox=box, horizontalalignment='left')

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


def units(vector):
    if vector == "jerk":
        return "m/s^3"
    elif vector == "accel":
        return "m/s^2"
    else:
        return ""


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

