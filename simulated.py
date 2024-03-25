from inputParams import parameters
from math import pow, sqrt
import time
import helpers as help
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare time, X and Y arrays
X = []
Y = []
t = np.linspace(0, tmax, int(tmax / dt))

# append x0 and y0
X.append(0) 
Y.append(y0)

def main():
    
    # calculate X and Y values
    for i in range(1, len(t)):
        newX, newY = newPoint(i, t[i-1])
        X.append(newX)
        Y.append(newY)

    # plot X and Y values
    plt.plot(X, Y, lw=3, color="tab:blue")
    plt.title("Simulated y(x) curve from kinematic equations")
    plt.ylim(0, y0+1)
    plt.xlim(0, help.xAxis(X, Y) + 1)
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.grid("both")

# t-notation is used because y'(x) can be written in terms of time with kinematic equations
def yprime(t):
    numerator = -1 * (accel(t)/g)
    denominator = sqrt(1 - pow(accel(t)/g, 2))
    return numerator/denominator


def accel(t):
    return a0 + (Jt * t)


def veloc(t):
    return v0 + (a0*t) + (0.5 * Jt * pow(t, 2))


def newPoint(i, t):
    # calculate parts shared by both x and y formulae in the numerators and denominators
    numerator = veloc(t) * dt
    denominator = sqrt(1 + pow(yprime(t), 2))

    # compute new X and Y values
    newX = X[i-1] + (numerator / denominator)
    newY = Y[i-1] + (yprime(t) * (numerator / denominator))
    return newX, newY


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Execution time: {round(time.time() - start, 2)} seconds")
    plt.show()