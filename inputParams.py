"""

This script allows you to pass in the initial conditions and arguments for rungekutta.py and simulated.py. Change the value of each variable in lines X through Y
to achieve the desired initial conditions and step size/time increments. The [main.py] script expects the data to arrive through this file and in dictionary-format used below.
If you change any input parameters here, make sure to make [main.py] compatible to these changes.

"""

# Jerk and jerk factor
tangentialJerk = 0.5
if tangentialJerk <= 0: jerkfactor = 1
else: jerkfactor = -1

# initial conditions
factorQ = 1
g = 9.81
initialAcceleration = 0.1
initialSpeed = 1
initialHeight = 100
xmax = 300
tmax = 15
stepSize = 0.001
timeIncrement = 0.001

parameters = {"j_t":  tangentialJerk, 
              "j_f": jerkfactor,
              "Q": factorQ, 
              "g": g, 
              "a_0": initialAcceleration, 
              "v_0": initialSpeed, 
              "y_0": initialHeight, 
              "xmax": xmax,
              "tmax": tmax,
              "h": stepSize,
              "dt": timeIncrement}

