from inputParams import parameters # type: ignore
from math import sqrt, pow

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