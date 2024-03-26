"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
import math
import matplotlib.pyplot as plt

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# y(x) plot features
def create_plot(type, X, Y):

    if type == "RK4":
        plt.plot(X, Y, lw=3, color="tab:red")
        plt.title("Runge-Kutta 4 y(x) curve")
    elif type == "simulated":
        plt.plot(X, Y, lw=3, color="tab:blue")
        plt.title("Simulated y(x) curve from kinematic equations")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.ylim(0, y0+1)
    try:  plt.xlim(0, xAxis(X, Y) + 1)
    except: plt.xlim(0, xmax + 1) 
    plt.grid("both")


# adaptive x-axis for better plot style
def xAxis(X, Y):
    
    # Find x-intercept 
    for index in range(len(Y)):
        print(Y[index])
        if math.isclose(Y[index], 0, abs_tol=0.1):
            Xintercept = X[index]
    
    return round(Xintercept)


