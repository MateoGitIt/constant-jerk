from rungekutta import rungekutta_main
from simulated import simulated_main
import pandas as pd
import csv


def verify_view_bounds(bounds):
    for b in bounds:
        if not isinstance(b, int) and not isinstance(b, float):
            exit("All bounds must integers or floating-point values.")
    if bounds[0] < bounds[1] and bounds[2] < bounds[3]:
        return bounds
    else:
        exit("Bounds are incorrect. Accepted format is [x1,x2,y1,y2] where x1 and y1 must "
             "be less than x2 and y2, respectively.")


def compute_curves():
    rk_X, rk_Y, U = rungekutta_main()
    kin_X, kin_Y = simulated_main()
    return {"rk4": [rk_X, rk_Y], "kinematics": [kin_X, kin_Y], "u_values": U}


def export_data(output_filename, data, file_format):
    if file_format == "xlsx":
        write_xlsx(output_filename, data)
    elif file_format == "csv":
        write_csv(output_filename, data)


def write_xlsx(filename, raw_data):
    data = format_data(raw_data)
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def write_csv(filename, raw_data):
    data = format_data(raw_data)
    length_rk = len(data["rk_X"])

    with open(filename, "w") as f:
        fieldnames = data.keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(length_rk):
            row = {
                "rk_X": data["rk_X"][i], 
                "rk_Y": data["rk_Y"][i],
                "U": data["U"][i],
                "ki_X": data["ki_X"][i],
                "ki_Y": data["ki_Y"][i]
                }
            writer.writerow(row)


def format_data(data):
    length_rk = len(data["rk4"][0])
    length_ki = len(data["kinematics"][0])

    if length_ki < length_rk:
        new_rk_data = {
        "rk_X": data["rk4"][0],
        "rk_Y": data["rk4"][1],
        "U": data["u_values"]
        }

        new_ki_X = [0] * length_rk
        new_ki_Y = [0] * length_rk
        for i in range(length_ki):
            new_ki_X[i] = data["kinematics"][0][i]
            new_ki_Y[i] = data["kinematics"][1][i]
        new_ki_data = {
            "ki_X": new_ki_X,
            "ki_Y": new_ki_Y
        }

    elif length_ki > length_rk:
        new_ki_data = {
            "ki_X": data["kinematics"][0],
            "ki_Y": data["kinematics"][1]
        }

        new_rk_X = [0] * length_ki
        new_rk_Y = [0] * length_ki
        new_U = [0] * length_ki
        for i in range(length_rk):
            new_rk_X[i] = data["rk"][0][i]
            new_rk_Y[i] = data["rk"][1][i]
            new_U[i] = data["u_values"][i]
        new_rk_data = {
            "rk_X": new_rk_X,
            "rk_Y": new_rk_Y,
            "U": new_U
        }
    return {**new_rk_data, **new_ki_data}

    