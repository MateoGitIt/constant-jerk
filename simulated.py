from inputParams import parameters
from math import pow, sqrt
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare time, X and Y arrays
X = []
Y = []
t = np.linspace(0, tmax, int(tmax / dt))

# append x0 and y0
X.append(0) # ---> I imagine the curve starts at horizontal position x = 0, right?
Y.append(y0)

def main():
    
    # calculate X and Y values
    for i in range(1, len(t)):
        newX, newY = newPoint(i, t[i-1])
        X.append(newX)
        Y.append(newY)

    # plot X and Y values
    plt.plot(X, Y, lw=2.5)
    plt.title("Simulated y(x) curve from kinematic equations")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.grid("both")
    plt.show()

# t-notation is used because y'(x) can be written in terms of time with kinematic equations
def yprime(t):
    numerator = -1 * (accel(t)/g)
    denominator = sqrt(1 - pow(accel(t)/g, 2))
    return numerator/denominator


def accel(t):
    return a0 + (Jt * t)


def veloc(t):
    return v0 + (a0*t) + (0.5 * Jt * pow(t, 2))

"""
Is y(x_i-1) accessing the i-th or the (i - 1)th time value? Is V_i-1 doing the same?

This current implementation accesses the (i-1)th value of each array
"""

def newPoint(i, t):
    # calculate parts shared by both x and y formulae in the numerators and denominators
    numerator = veloc(t) * dt
    denominator = sqrt(1 + pow(yprime(t), 2))

    # compute new X and Y values
    newX = X[i-1] + (numerator / denominator)
    newY = Y[i-1] + (yprime(t) * (numerator / denominator))
    return newX, newY


if __name__ == "__main__":
    main()