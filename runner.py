"""
This file is the easiest way to interact with the functionalities of the simulation software and other features we
implemented. You will find four sections below to provide inputs: side-by-side plots, hodograph, best-fit curve, and
view. This "runner.py" file calls other files in this repository to achieve the desired output.

"""

from helpers import create_plot
import matplotlib.pyplot as plt

# SIDE-BY SIDE PLOTS
# what would another researcher like to see from the curve?
plots = ["RK4", "kinematics"]
rows = 1
columns = 2
fig, axs = plt.subplots(rows, columns)
for i, ax in enumerate(axs):
    create_plot(plots[i], ax, data=[X, Y])


# BEST-FIT CURVE
best_fit_model = ["3_poly", "2_poly"]
initial_guess = [[1, 1, 1, 1], [1, 1, 1]]

"""

Availaible hodographs types: 
1) "jerk", "accel" (total vectors, no components), 
2) "jerk_comp", "accel_comp", (total vectors w/ xy components)
3) "jerk_tan_norm" , "accel_tan_norm" (total vectors w/ tangential and normal components)

"""

hodograph_type = ""
frames = 100
pause = 0.1

# VIEW
view = [-100, 100, -100, 100]

# DIVERGENCE POINT AND MOTION
divergence_motion = True

# CSV OUTPUT FILE
create_csv_file = True
