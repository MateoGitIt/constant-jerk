"""
This file is the easiest way to interact with the functionalities of the simulation software and other features we
implemented. You will find four sections below to provide inputs: side-by-side plots, hodograph, best-fit curve, and
view. This "runner.py" file calls other files in this repository to achieve the desired output.

"""

from helpers import create_plot, set_view
from helpers_runner import verify_view_bounds
from rungekutta import rungekutta_main
import matplotlib.pyplot as plt

# SIDE-BY SIDE PLOTS
# what would another researcher like to see from the curve?
plots = ["RK4", "kinematics"]
rows = 1
columns = 2
fig, axs = plt.subplots(rows, columns)
for i, ax in enumerate(axs):
    # How to manage and receive what data the user wants to plot? First, what else could the user want to plot?
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
view_bounds = [-100, 100, -100, 100]
if verify_view_bounds(view_bounds):
    for ax in axs:
        set_view(ax, view_bounds)

# DIVERGENCE POINT AND MOTION
divergence_motion = True

# CSV OUTPUT FILE
create_csv_file = True
