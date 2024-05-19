"""

Availaible hodographs types: 
1) "jerk", "accel" (total vectors, no components), 
2) "jerk_xy", "accel_xy", (total vectors w/ xy components)
3) "jerk_tan_norm" , "accel_tan_norm" (total vectors w/ tangential and normal components)

"""

from helpers import create_plot, set_view, divergence_point, create_fit_curve, create_hodograph
from helpers_runner import verify_view_bounds, compute_curves
import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2)
data = compute_curves()
view_bounds = [-500, 1500, -1500, 500]

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data["rk4"][0], data["rk4"][1], data["u_values"])

hodograph_type = "jerk"
scale = 200
frames = 100
pause = 0.0001
fig.canvas.mpl_connect("close_event", exit)
create_hodograph("rk4", hodograph_type, axs[0], data["rk4"][0], data["rk4"][1], U=data["u_values"], div=(True, *div_data),
                    frame_num=frames, pause_length=pause, view=view_bounds, scale=scale)
create_hodograph("kinematics", hodograph_type, axs[1], data["kinematics"][0], data["kinematics"][1], U=data["u_values"],
                    frame_num=frames, pause_length=pause, view=view_bounds, scale=scale)

plt.show()