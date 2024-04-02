from inputParams import parameters
from math import pow, sqrt
from sys import exit, argv
from helpers import create_plot, Uprime
import hodograph
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

# hodograph (true/false)
hodo = False
if len(argv) == 2 and argv[1] == "hodograph":
    hodo = True

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

    return X, Y, U


def rungekutta_kvalues(u, y_i):
    k1 = Uprime(u, y_i)
    k2 = Uprime(u + (h * (k1/2)), y_i)
    k3 = Uprime(u + (h * (k2/2)), y_i)
    k4 = Uprime(u + (h * k3), y_i)
    return k1, k2, k3, k4


if __name__ == "__main__":
    start =  time.time()
    try:
        main()
    except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
        
    print(f"RK4 execution time: {round(time.time() - start, 2)} seconds")

    # create plot
    if hodo: create_plot("RK4", X, Y, y_slopes=U, hodograph=True, frames=1000, pause=0.1)
    else: create_plot("RK4", X, Y, hodograph=False)
