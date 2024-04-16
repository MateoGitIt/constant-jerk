from inputParams import parameters # type: ignore
from components import veloc_xcomp, veloc_ycomp
from math import sqrt, pow
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

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


def parabolic_free_fall(divPoint, speed, u, duration):
    t = np.linspace(0, duration, int(duration / dt))
    X = list(range(len(t)))
    Y = list(range(len(t)))
    for i, t in enumerate(t):
        X[i] = divPoint[0] + veloc_xcomp(u, speed) * t
        Y[i] = divPoint[1] + veloc_ycomp(u, speed) * t - (g/2) * pow(t, 2)
    return X, Y

