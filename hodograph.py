"""

Availaible hodographs types: 
1) "jerk", "accel" (total vectors, no components), 
2) "jerk_xy", "accel_xy", (total vectors w/ xy components)
3) "jerk_tan_norm" , "accel_tan_norm" (total vectors w/ tangential and normal components)

"""

from helpers import create_plot, set_view, divergence_point, create_fit_curve, create_hodograph
from helpers_runner import verify_view_bounds, compute_curves
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
data = compute_curves()
view_bounds = [-100, 1500, -1500, 100]

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data["rk4"][0], data["rk4"][1], data["u_values"])

# flip the vectors

vectors = [("jerk", "xy"), ("accel", "tangnorm")]
hodograph_vectors = "jerk_tang_norm"
scale = 250
frames = 150
pause = 0.001
fig.canvas.mpl_connect("close_event", exit)
create_hodograph("rk4", hodograph_vectors, ax, data["rk4"][0], data["rk4"][1], U=data["u_values"], div=(True, *div_data),
                    frame_num=frames, pause_length=pause, view=verify_view_bounds(view_bounds), scale=scale)

plt.show()