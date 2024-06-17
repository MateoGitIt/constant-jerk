from inputParams import parameters
from math import sqrt, pow, sin, cos, atan
from computations import Uprime, speed, Udoubleprime
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt, rounding_decimals = parameters.values()
U_origins_cpy = None
Y_origins_cpy = None
X_origins_cpy = None


def t_hat(u):
    Tx = 1 / sqrt(1 + pow(u, 2))
    Ty = u / sqrt(1 + pow(u, 2))
    return np.array([Tx, Ty])


def n_hat(u):
    Nx = (-1 * u) / sqrt(1 + pow(u, 2))
    Ny = 1 / sqrt(1 + pow(u, 2))
    return np.array([Nx, Ny])


def accel_xcomp(u, y):
    common_factor = u / (1 + pow(u, 2))
    third_fraction = pow(speed(u, y), 2) * Uprime(u, y) / (1 + pow(u, 2))
    if Jt < 0: third_fraction = -1*third_fraction # CHECK SIGN LOGIC
    return common_factor * (-1*(g/Q) - third_fraction)


def accel_ycomp(u, y):
    common_factor = 1 / (1 + pow(u, 2))
    first_term = (-1 * g * pow(u, 2)) / Q
    second_term = (pow(speed(u, y), 2) * Uprime(u, y)) / (1 + pow(u, 2))
    return common_factor * (first_term + second_term)


def tangential_accel(u, y):
    x_tan = -(g/Q) * (u / (1 + pow(u, 2)))
    y_tan = -(g/Q) * (pow(u, 2) / (1 + pow(u, 2)))
    magnitude = sqrt(pow(x_tan, 2) + pow(y_tan, 2))
    return np.array([x_tan, y_tan]), magnitude


def tangential_accel2(u, y):
    magnitude = (-g / Q) * (u / sqrt(1 + pow(u, 2)))
    return magnitude * t_hat(u), magnitude


def normal_accel(u, y):
    common_factor = Jf*abs((Uprime(u, y) * pow(speed(u, y), 2)) / pow(1 + pow(u, 2), 3/2))
    x_norm = common_factor * (-1) * u / sqrt(1 + pow(u, 2))
    y_norm = common_factor / sqrt(1 + pow(u, 2))
    return np.array([x_norm, y_norm]), sqrt(pow(x_norm, 2) + pow(y_norm, 2))


def normal_accel2(u, y):
    magnitude = Jf*abs(pow(speed(u, y), 2) * Uprime(u, y) / pow(1 + pow(u, 2), 3/2))
    return magnitude * n_hat(u), magnitude


def jerk_xcomp(u, y):
    return (tangential_jerk(u, y)[1] * t_hat(u)[0]) + (normal_jerk(u, y)[1] * n_hat(u)[0])


def jerk_ycomp(u, y):
    return (tangential_jerk(u, y)[1] * t_hat(u)[1]) + (normal_jerk(u, y)[1] * n_hat(u)[1])


def tangential_jerk(u, y):
    common_factor = (Uprime(u, y) * speed(u, y)) / pow(1 + pow(u, 2), 2)
    second_term = Jf*(Uprime(u, y) * pow(speed(u, y), 2)) / (1 + pow(u, 2))
    magnitude = common_factor * (-1*g - second_term)
    return magnitude * t_hat(u), magnitude


def normal_jerk(u, y):
    first_common_factor = (Jf * pow(speed(u, y), 3) * sqrt(pow(Uprime(u, y), 2))) / (pow(1 + pow(u, 2), 2))
    first_term = (-2 * g * u) / pow(speed(u, y), 2)
    second_term = ((Udoubleprime(U_origins_cpy, Y_origins_cpy, X_origins_cpy, u, y) * (1 + pow(u, 2))) - 3 * u * pow(Uprime(u, y), 2)) / (Uprime(u, y) * (1 + pow(u, 2)))
    third_term = (g * u * Uprime(u, y) * speed(u, y)) / pow(1 + pow(u, 2), 2)
    magnitude = first_common_factor * (first_term + second_term) - third_term
    return magnitude * n_hat(u), magnitude


def components_file_local_copy(U_origins, Y_origins, X_origins):
    global U_origins_cpy, Y_origins_cpy, X_origins_cpy
    U_origins_cpy = U_origins.copy()
    Y_origins_cpy = Y_origins.copy()
    X_origins_cpy = X_origins.copy()


def vector_xy(vector, frame_num, U_origins, Y_origins, X_origins):
    components_file_local_copy(U_origins, Y_origins, X_origins)

    # table of component functions
    x_comp_funcs = {"accel": accel_xcomp, "jerk": jerk_xcomp}
    y_comp_funcs = {"accel": accel_ycomp, "jerk": jerk_ycomp}
    X_comp = np.empty(frame_num)
    Y_comp = np.empty(frame_num)

    # note the number of components per list equals frame_num
    for i in range(frame_num):
        X_comp[i] = x_comp_funcs[vector](U_origins[i], Y_origins[i])
        Y_comp[i] = y_comp_funcs[vector](U_origins[i], Y_origins[i])
    return X_comp, Y_comp


def vector_tang_norm(vector, frame_num, U_origins, Y_origins, X_origins):
    # Allow other normal_jerk to call Udoubleprime
    components_file_local_copy(U_origins, Y_origins, X_origins)

    tan_comp_funcs = {"accel": tangential_accel2, "jerk": tangential_jerk}
    norm_comp_funcs = {"accel": normal_accel2, "jerk": normal_jerk}
    tang = np.empty((frame_num, 2))
    norm = np.empty((frame_num, 2))

    for i in range(frame_num):
        tang[i] = tan_comp_funcs[vector](U_origins[i], Y_origins[i])[0]
        norm[i] = norm_comp_funcs[vector](U_origins[i], Y_origins[i])[0]
    return tang, norm


def vector_xy_point(vector, i, X, Y, U):
    if vector == "jerk": components_file_local_copy(U, Y, X)
    x_comp_funcs = {"accel": accel_xcomp, "jerk": jerk_xcomp}
    y_comp_funcs = {"accel": accel_ycomp, "jerk": jerk_ycomp}
    x_comp = x_comp_funcs[vector](U[i], Y[i])
    y_comp = y_comp_funcs[vector](U[i], Y[i])
    return x_comp, y_comp, sqrt(pow(x_comp, 2) + pow(y_comp, 2))

def vector_tang_norm_point(vector, i, X, Y, U):
    if vector == "jerk": components_file_local_copy(U, Y, X)
    tan_comp_funcs = {"accel": tangential_accel2, "jerk": tangential_jerk}
    norm_comp_funcs = {"accel": normal_accel2, "jerk": normal_jerk}
    tan_comp = tan_comp_funcs[vector](U[i], Y[i])[1]
    norm_comp = norm_comp_funcs[vector](U[i], Y[i])[1]
    return tan_comp, norm_comp, sqrt(pow(tan_comp, 2) + pow(norm_comp, 2))

def veloc_xcomp(u, speed):
    return abs(speed) * cos(atan(u))


def veloc_ycomp(u, speed):
    return abs(speed) * sin(atan(u))

