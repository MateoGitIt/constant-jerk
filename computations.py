from inputParams import parameters # type: ignore
from math import sqrt, pow, sin, cos, atan
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# right-hand side of the autonomous differential equation for y''(x) = U'(x)
def Uprime(u, y):
    factor1 = Jf * (1 + pow(u, 2)) / (2 * pow(speed(u, y), 2))
    radicand = pow(g/Q, 2) - (Jf * 4 * speed(u, y) * Jt * (1 + pow(u, 2)))
    factor2 = (-1 * g/Q) + sqrt(radicand)
    return factor1 * factor2
    # CHECK THIS FORMULA; IT MIGHT NOT BE THE SAME AS THE ONE IN THE GOOGLE DOCS

# speed as a function of y
def speed(u, y):
    second_term = 2 * g * (y0 - (y +(u*h))) / Q
    return sqrt(pow(v0, 2) + second_term)


def parabolic_free_fall(divPoint, speed, u, duration):
    t = np.linspace(0, duration, int(duration / dt))
    X = list(range(len(t)))
    Y = list(range(len(t)))
    for i, t in enumerate(t):
        X[i] = divPoint[0] + (abs(speed) * cos(atan(u))) * t
        Y[i] = divPoint[1] + (abs(speed) * sin(atan(u))) * t - (g/2) * pow(t, 2)
    return X, Y


def Udoubleprime():
    pass