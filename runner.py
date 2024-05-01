"""
This file is the easiest way to interact with the functionalities of the simulation software and other features we
implemented. You will find four sections below to provide inputs: side-by-side plots, hodograph, best-fit curve, and
view. This "runner.py" file calls other files in this repository to achieve the desired output.

"""

from helpers import create_plot, set_view
from helpers_runner import verify_view_bounds
from rungekutta import rungekutta_main
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2)

# VIEW: READY
view = True
view_bounds = [-100, 100, -100, 100]
if view and verify_view_bounds(view_bounds):
    for ax in axs:
        set_view(ax, view_bounds)

# PLOTS AND HODOGRAPH
hodo = True
hodograph_type = ""
frames = 100
pause = 0.1

X, Y, U = rungekutta_main()
plots = ["RK4", "kinematics"]
for i, ax in enumerate(axs[0]): # axs[0] yields top row
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


# DIVERGENCE POINT AND MOTION
divergence_motion = True

# CSV OUTPUT FILE
create_csv_file = True
output_filename = "test.csv"

