from helpers import create_plot, set_view, divergence_point, create_fit_curve, create_hodograph
from helpers_runner import verify_view_bounds, compute_curves
import matplotlib.pyplot as plt

# BEST-FIT MODEL: READY
# CSV OUTPUT FILE: NOT DONE
# DIVERGENCE MOTION: READY
# STATIC PLOTS: READY
# SET VIEW: READY

fig, axs = plt.subplots(1, 2)
data = compute_curves()
view_bounds = [-500, 1500, -1500, 500]

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data["rk4"][0], data["rk4"][1], data["u_values"])

best_fit = True
best_fit_models = {"3_poly": [1, 1, 1, 1], "2_poly": [1, 1, 1], "5_poly": [1, 1, 1, 1, 1, 1]}

plots = ["rk4", "kinematics"]

for i, ax in enumerate(axs): # axs[0] yields top row
    create_plot(plots[i], ax, data=data[plots[i]], div=(divergence_motion, *div_data))
    if best_fit:
        for model in list(best_fit_models.keys()):
            create_fit_curve(model, ax, best_fit_models[model], view_bounds[0], view_bounds[1], data=data[plots[i]], curve_tag=plots[i])
    ax.legend()

view = True
if view and verify_view_bounds(view_bounds):
    for ax in axs:
        set_view(ax, view_bounds)


# CSV OUTPUT FILE: TBD
create_csv_file = True
output_filename = "test.csv"

plt.show()