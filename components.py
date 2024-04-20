from inputParams import parameters
from math import sqrt, pow, sin, cos, atan
from computations import Uprime, speed, Udoubleprime
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()


def t_hat(u):
    return (1 / sqrt(1 + pow(u, 2))) * np.array([1, u])


def n_hat(u):
    return (1 / sqrt(1 + pow(u, 2))) * np.array([-1 * u, 1])


def accel_xcomp(u, y):
    common_factor = u / (1 + pow(u, 2))
    third_fraction = pow(speed(u, y), 2) * Uprime(u, y) / (1 + pow(u, 2))
    if Jt < 0: third_fraction = -1*third_fraction # CHECK SIGN LOGIC
    return common_factor * (-1*(g/Q) - third_fraction)


def accel_ycomp(u, y):
    common_factor = 1 / (1 + pow(u, 2))
    first_term = (-1 * g * pow(u, 2)) / Q
    second_term = (pow(speed(u, y), 2) * Uprime(u, y)) / (1 + pow(u, 2))
    if Jt < 0: second_term = -1*second_term
    return common_factor * (first_term + second_term)


def tangential_accel(u, y):
    x_tan = -(g/Q) * (u / (1 + pow(u, 2)))
    y_tan = -(g/Q) * (pow(u, 2) / (1 + pow(u, 2)))
    return np.array([x_tan, y_tan]), sqrt(pow(x_tan, 2) + pow(y_tan, 2))


def normal_accel(u, y):
    common_factor = pow(speed(u, y), 2) * Uprime(u, y) / pow(1 + pow(u, 2), 2)
    if Jt < 0: common_factor = -1*common_factor # CHECK SIGN LOGIC
    x_norm = common_factor * (-1 * u)
    y_norm = common_factor
    return np.array([x_norm, y_norm]), sqrt(pow(x_norm, 2) + pow(y_norm, 2))


def jerk_xcomp(u, y):
    return (tangential_jerk(u, y)[1] * t_hat(u)[0]) + (normal_jerk(u, y)[1] * n_hat(u)[0])


def jerk_ycomp(u, y):
    return (tangential_jerk(u, y)[1] * t_hat(u)[1]) + (normal_jerk(u, y)[1] * n_hat(u)[1])


def tangential_jerk(u, y):
    common_factor = (Uprime(u, y) * speed(u, y)) / pow(1 + pow(u, 2), 2)
    second_term = (Uprime(u, y) * pow(speed(u, y), 2)) / (1 + pow(u, 2))
    magnitude = common_factor * (-1 * (g/Q) - second_term)
    return magnitude * t_hat(u), magnitude


# TO DO: IMPLEMENT Udoubleprime functions for NORMAL JERK
def normal_jerk(u, y):
    first_common_factor = speed(u, y) / pow(1 + pow(u, 2), 2)
    first_term = Udoubleprime() * pow(speed(u, y), 2)
    second_common_factor = -3 * Uprime(u, y) * u
    innermost_paren = (g/Q) + (Uprime(u, y) * pow(speed(u, y), 2) / (1 + pow(u, 2)))
    magnitude = first_common_factor * (first_term - second_common_factor*(innermost_paren))
    return magnitude * n_hat(u), magnitude


def veloc_xcomp(u, speed):
    return abs(speed) * cos(atan(u))


def veloc_ycomp(u, speed):
    return abs(speed) * sin(atan(u))

