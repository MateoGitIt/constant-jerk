"""

This file implements functions used by other files in this repository. These functions are auxiliary and are imported to 
the primary scripts rungekutta.py and simulation.py.

"""

from inputParams import parameters
import math

# unpack inputs from "inputParams.py"
Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt = parameters.values()

# adaptive x-axis for better plot style
def xAxis(X, Y):
    
    # Find x-intercept 
    for index in range(len(Y)):
        print(Y[index])
        if math.isclose(Y[index], 0, abs_tol=0.1):
            Xintercept = X[index]
    
    return round(Xintercept)


