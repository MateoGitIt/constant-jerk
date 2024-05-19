"""
This file is the easiest way to interact with the functionalities of the simulation software and other features we
implemented. You will find four sections below to provide inputs: side-by-side plots, hodograph, best-fit curve, and
view. This "runner.py" file calls other files in this repository to achieve the desired output.

"""

from helpers import create_plot, set_view, divergence_point, create_fit_curve, create_hodograph
from helpers_runner import verify_view_bounds, compute_curves
import matplotlib.pyplot as plt

# BEST-FIT MODEL: READY
# HODOGRAPH: NOT DONE
# ANIMATION (3RD ROW): NOT READY
# CSV OUTPUT FILE: NOT DONE
# DIVERGENCE MOTION: READY
# STATIC PLOTS: READY
# SET VIEW: READY

fig, axs = plt.subplots(2, 2)
data = compute_curves()
view_bounds = [-500, 1500, -1500, 500]

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data["rk4"][0], data["rk4"][1], data["u_values"])

best_fit = True
best_fit_models = {"3_poly": [1, 1, 1, 1], "2_poly": [1, 1, 1], "5_poly": [1, 1, 1, 1, 1, 1]}

plots = ["rk4", "kinematics"]

for i, ax in enumerate(axs[0]): # axs[0] yields top row
    create_plot(plots[i], ax, data=data[plots[i]], div=(divergence_motion, *div_data))
    if best_fit:
        for model in list(best_fit_models.keys()):
            create_fit_curve(model, ax, best_fit_models[model], view_bounds[0], view_bounds[1], data=data[plots[i]], curve_tag=plots[i])
    ax.legend()


# HODOGRAPH
"""

Availaible hodographs types: 
1) "jerk", "accel" (total vectors, no components), 
2) "jerk_xy", "accel_xy", (total vectors w/ xy components)
3) "jerk_tan_norm" , "accel_tan_norm" (total vectors w/ tangential and normal components)

"""

view = True
if view and verify_view_bounds(view_bounds):
    for ax in axs[0]:
        set_view(ax, view_bounds)
    
hodo = True
hodograph_type = "accel_xy"
frames = 350
pause = 0.0001
fig.canvas.mpl_connect("close_event", exit)

if hodo:
    create_hodograph("rk4", hodograph_type, axs[1][0], data["rk4"][0], data["rk4"][1], U=data["u_values"],
                     frame_num=frames, pause_length=pause, view=view_bounds)
    create_hodograph("kinematics", hodograph_type, axs[1][0], data["kinematics"][0], data["kinematics"][1], U=data["u_values"],
                     frame_num=frames, pause_length=pause, view=view_bounds)

# CSV OUTPUT FILE: TBD
create_csv_file = True
output_filename = "test.csv"

plt.show()