"""

This script allows you to pass in the initial conditions and arguments for [main.py]. Change the value of each variable in lines X through Y
to achieve the desired initial conditions and step size. The [main.py] script expects the data to arrive through this file and in dictionary-format used below.
If you change any input parameters here, make sure to make [main.py] compatible to these changes.

The [main.py] script expects values for tangential jerk (tangentialJerk), Q (factorQ), g (gravityAccel), initial speed (initialSpeed), and step size for 
the Runge-Kutta method.

"""

tangentialJerk = 1
factorQ = 1
g = 9.81
initialSpeed = 1
stepSize = 0.001

parameters = {"j_t":  tangentialJerk, "Q": factorQ, "g": g, "v_0": initialSpeed, "h": stepSize}
