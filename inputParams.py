"""

This script allows you to pass in the initial conditions and arguments for rungekutta.py and simulated.py. Change the value of each variable in lines X through Y
to achieve the desired initial conditions and step size/time increments. The [main.py] script expects the data to arrive through this file and in dictionary-format used below.
If you change any input parameters here, make sure to make [main.py] compatible to these changes.

"""

tangentialJerk = 10
factorQ = 1
g = 9.81
initialAcceleration = 0
initialSpeed = 1
initialHeight = 1
xmax = 8
tmax = 2
stepSize = 0.0001
timeIncrement = 0.00001

parameters = {"j_t":  tangentialJerk, 
              "Q": factorQ, 
              "g": g, 
              "a_0": initialAcceleration, 
              "v_0": initialSpeed, 
              "y_0": initialHeight, 
              "xmax": xmax,
              "tmax": tmax,
              "h": stepSize,
              "dt": timeIncrement}


"""
Smallest step size successfully tried: 0.000001
"""