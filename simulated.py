from inputParams import parameters
from math import pow, sqrt
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare time, velocity, X and Y arrays
X = np.array()
Y = np.array()
veloc = np.array()
t = np.linspace(0, tmax, dt)

# append x0 and y0
X.append(0) # ---> Does the curve starts at horizontal position x = 0?
Y.append(y0)

def main():
    



# t-notation is used because y'(x) can be written in terms of time with kinematic equations
def yprime(t):
    numerator = -1 * (accel(t)/g)
    denominator = sqrt(1 - pow(accel(t)/g, 2))
    return numerator/denominator


def accel(t):
    return a0 + (Jt * t)


def veloc(t):
    return v0 + (a0*t) + (0.5 * Jt * pow(t, 2))


# newX and newY take in index i to access i - 1 X and Y values

"""
Is y(x_i-1) accessing the i-th or the (i - 1)th time value?
I figure it has to access the i-th time value (the time value of the current iteration), otherwise it'd access
out-of-bounds values in the first iteration (where t[0] = 0)

"""
def newX(i, t):
    numerator = veloc(t[i]) * dt
    denominator = sqrt(1 + pow(yprime(t[i]), 2))
    return X[i-1] + (numerator / denominator)
    

def newY(i, t):
    numerator = veloc(t[i]) * yprime(t[i]) * dt
    denominator = sqrt(1 + pow(yprime(t[i]), 2))
    return Y[i-1] + (numerator / denominator)


if __name__ == "__main__":
    main()