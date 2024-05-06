"""
This file is the easiest way to interact with the functionalities of the simulation software and other features we
implemented. You will find four sections below to provide inputs: side-by-side plots, hodograph, best-fit curve, and
view. This "runner.py" file calls other files in this repository to achieve the desired output.

"""

from helpers import create_plot, set_view, divergence_point
from helpers_runner import verify_view_bounds, compute_curves
import matplotlib.pyplot as plt

# FEATURES:
# DIVERGENCE MOTION: READY
# BEST-FIT MODEL: NOT DONE
# STATIC PLOTS: READY
# HODOGRAPH: NOT DONE
# SET VIEW: READT
# CSV OUTPUT FILE: NOT DONE

fig, axs = plt.subplots(2, 2)
data = compute_curves()

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data[0][0], data[0][1], data[2])

# BEST-FIT CURVE: TDB - MAKE IT SO THAT THE BEST-FIT CURVES ARE ONLY SHOWN IN THE TOP-ROW PLOTS. LEAVE THE BOTTOM PLOTS CLEAN FOR THE HODOGRAPH.
best_fit = True
best_fit_model = ["3_poly", "2_poly"]
initial_guess = [[1, 1, 1, 1], [1, 1, 1]]

plots = ["RK4", "kinematics"]
for i, ax in enumerate(axs[0]): # axs[0] yields top row
    create_plot(plots[i], ax, data=data[i], div=(divergence_motion, *div_data))

# HODOGRAPH: BOTTOM TWO 
hodo = True
hodograph_type = ""
frames = 100
pause = 0.1

"""

Availaible hodographs types: 
1) "jerk", "accel" (total vectors, no components), 
2) "jerk_xy", "accel_xy", (total vectors w/ xy components)
3) "jerk_tan_norm" , "accel_tan_norm" (total vectors w/ tangential and normal components)

"""

# VIEW: READY
view = True
view_bounds = [-100, 1000, -1000, 100]
if view and verify_view_bounds(view_bounds):
    for ax in axs[0]:
        set_view(ax, view_bounds)

# CSV OUTPUT FILE: TBD
create_csv_file = True
output_filename = "test.csv"

plt.show()