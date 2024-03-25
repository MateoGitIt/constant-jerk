from inputParams import parameters
from math import pow, sqrt
from sys import exit
import helpers as help
import time
import matplotlib.pyplot as plt
import numpy as np

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare array for U_i, Y_i, and x_i values
U = []
Y = []
X = np.linspace(0, xmax, int(xmax / h)) 
X = X.tolist()

# append initial height
Y.append(y0)

# calculate U0 (which equals y'(x) at t = 0) and append to U array
U0 = -1 * (a0/g) / sqrt(1 - pow(a0/g, 2))
U.append(U0)

def main():

    # calculate new U and Y values and record them in lists
    for i in range(1, len(X)):
        k1, k2, k3, k4 = rungekutta_kvalues(U[i-1], Y[i-1])
        new_U = U[i-1] + (h/6)*(k1 + (2*k2) + (2*k3) + k4)
        U.append(new_U)
        new_Y = Y[i-1] + (U[i-1] * h)
        Y.append(new_Y)

    # plot curve of values X and Y
    plt.plot(X, Y, lw=3, color="tab:red")
    plt.title("Runge-Kutta 4 y(x) curve")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.ylim(0, y0+1)
    try:  plt.xlim(0, help.xAxis(X, Y) + 1)
    except: plt.xlim(0, xmax + 1) 
    plt.grid("both")


# right-hand side of the autonomous differential equation
def func(u, y_i):

    factor1 = Jf * (1 + pow(u, 2)) / (2 * pow(veloc(u, y_i), 2))
    radicand = pow(g/Q, 2) - (Jf * 4 * veloc(u, y_i) * Jt * (1 + pow(u, 2)))
    factor2 = (-1 * g/Q) + sqrt(radicand)
    return factor1 * factor2
        

def veloc(u, y_i):
    second_term = 2 * g * (y0 - (y_i +(u*h))) / Q
    return sqrt(pow(v0, 2) + second_term)


def rungekutta_kvalues(u, y_i):
    k1 = func(u, y_i)
    k2 = func(u + (h * (k1/2)), y_i)
    k3 = func(u + (h * (k2/2)), y_i)
    k4 = func(u + (h * k3), y_i)
    return k1, k2, k3, k4


if __name__ == "__main__":
    start =  time.time()
    try:
        main()
        print(f"Execution time: {round(time.time() - start, 2)} seconds")
    except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
        
    plt.show()