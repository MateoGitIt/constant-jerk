from inputParams import parameters
from math import sqrt, pow

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

def accel_xcomp(u):
    return


def accel_ycomp(test):
    return test


def accel_tancomp(u):
    x_comp = -(g/Q) * (u / (1 + pow(u, 2)))
    y_comp = -(g/Q) * (pow(u, 2) / (1 + pow(u, 2)))
    return x_comp, y_comp


def accel_normcomp(test):
    return test, test


def jerk_xcomp(test):
    return test


def jerk_ycomp(test):
    return test


def jerk_tancomp(test):
    return test, test


def jerk_normcomp(test):
    return test, test