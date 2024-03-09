from inputParams import parameters
from math import pow, sqrt
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare time, X and Y arrays
X = np.array()
Y = np.array()
t = np.linspace(0, tmax, dt)

def main():
    pass
    


# t-notation is used because y'(x) can be written in terms of time with kinematic equations
def yprime(t):
    numerator = -1 * (a0/g)
    denominator = sqrt(1 - pow(a0/g, 2))
    return numerator/denominator


def accel(t):
    return a0 + (Jt * t)


def vel(t):
    return v0 + (a0*t) + (0.5 * Jt * pow(t, 2))


if __name__ == "__main__":
    main()