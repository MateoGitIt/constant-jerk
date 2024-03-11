from inputParams import parameters
from math import pow, sqrt
from sys import exit
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare array for U_i, Y_i, and x_i values
U = []
Y = []
X = np.linspace(0, xmax, int(xmax / h)) 
X = X.tolist()

# append initial height
Y.append(y0)

# calculate U0 (which equals y'(x) at t = 0) and append to U array; SHOULD WE INCLUDE Q IN THE DENOMINATOR? PAPER DOESN'T, jerk2mp.py DOES
U0 = -1 * (a0/g) / sqrt(1 - pow(a0/g, 2))
U.append(U0)

def main():

    # calculate new U-values and record them
    for i in range(1, len(X)):
        k1, k2, k3, k4 = rungekutta_kvalues(U[i-1])
        new_U = U[i-1] + (h/6)*(k1 + (2*k2) + (2*k3) + k4)
        U.append(new_U)

    # calculated y(x) from u(x) = y´(x)
    for i in range(1, len(X)):
        new_Y = Y[i-1] + (U[i-1] * h)
        Y.append(new_Y)

    # plot curve of values X and Y
    plt.plot(X, Y, lw=3, color="tab:red")
    plt.title("Runge-Kutta 4 y(x) curve")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.ylim(0, y0+1)
    plt.xlim(0, xmax+1)
    plt.grid("both")
    plt.show()


# right-hand side of the autonomous differential equation
def func(u):

    # when initial conditions are invalid, they typically create an error in this line
    try:
        numerator = -1 * Jt * Q * pow(1 + pow(u, 2), 2) 
    except OverflowError as e:
        exit(f"OverflowError: {e}.\nInitial conditions may not be valid or cause some " 
             "equations to break down mathematically.\nInputting smaller xmax, initial acceleration, " 
             "or jerk values may resolve this error.")
        
    denominator = g * sqrt(pow(v0, 2) - (2/Q) * g * h * u)
    return numerator/denominator


def rungekutta_kvalues(u):
    k1 = func(u)
    k2 = func(u + (h * (k1/2)))
    k3 = func(u + (h * (k2/2)))
    k4 = func(u + (h * k3))
    return k1, k2, k3, k4


if __name__ == "__main__":
    main()