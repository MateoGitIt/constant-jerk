from inputParams import parameters
from math import pow, sqrt
from sys import exit, argv
from helpers import create_plot, create_hodograph, hodograph_inputs, view_inputs
import time
import matplotlib.pyplot as plt
import numpy as np

"""

COMMAND-LINE USE: python simulated.py [vector] [frame_number] [pause_length]

"""

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# declare time, X and Y arrays
X = []
Y = []
t = np.linspace(0, tmax, int(tmax / dt))

# append x0 and y0
X.append(0) 
Y.append(y0)


# INPUT: macroscopic view option
view = False
bounds = []
if len(argv) == 3 and argv[1] == "view":
    bounds, view = view_inputs(argv)
    
# INPUT: hodograph
hodo = False
if len(argv) == 4:
    hodo, frame_num, pause_length = hodograph_inputs(argv)


def main():
    
    # calculate X and Y values
    for i in range(1, len(t)):
        newX, newY = newPoint(i, t[i-1])
        X.append(newX)
        Y.append(newY)
    
    return X, Y

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
    try:
        main()
    except Exception as e:
        exit(f"An error occured: {e}. Physically impossible initial conditions "
             "may cause some equations to break down. Try different initial conditions.")
        
    print(f"Kinematic simulation execution time: {round(time.time() - start, 2)} seconds")

    # create plot
    fig, ax = plt.subplots(1, 1)
    fig.canvas.mpl_connect("close_event", exit)
    if hodo: create_hodograph("simulated", argv[1], ax, X, Y, frame_num=frame_num, pause_length=pause_length)
    else: 
        create_plot("simulated", ax, X, Y, view=view, bounds=bounds)
        plt.show() 