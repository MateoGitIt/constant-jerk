from helpers import create_plot, divergence_point, create_fit_curve
from helpers_runner import verify_view_bounds, compute_curves, export_data
import matplotlib.pyplot as plt

# THIS FILE IS FULLY READY. CURVE DISPLAYING IS COMPLETE.

fig, axs = plt.subplots(1, 2)
data = compute_curves()
view_bounds = [-500, 1500, -1500, 500]

# DIVERGENCE POINT AND TRAJECTORY
divergence_motion = True
div_data = divergence_point(data["rk4"][0], data["rk4"][1], data["u_values"])

best_fit = True
view = True
textbox = True
best_fit_models = {"3_poly": [1, 1, 1, 1], "2_poly": [1, 1, 1], "5_poly": [1, 1, 1, 1, 1, 1]}
plots = ["rk4", "kinematics"]

for i, ax in enumerate(axs):
    create_plot(plots[i], ax, data=data[plots[i]], div=(divergence_motion, *div_data), view=(view, *verify_view_bounds(view_bounds)),
                show_textbox=textbox)
    if best_fit:
        for model in list(best_fit_models.keys()):
            create_fit_curve(model, ax, best_fit_models[model], view_bounds[0], view_bounds[1], data=data[plots[i]], curve_tag=plots[i])
    ax.legend()


create_output_file = False
output_filename = "negjerk.xlsx"
file_format = "xlsx"
if create_output_file:
    export_data(output_filename, data, file_format)

plt.show()