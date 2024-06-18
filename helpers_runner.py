from rungekutta import rungekutta_main
from simulated import simulated_main
from components import tangential_accel2, normal_accel2, tangential_jerk, normal_jerk, components_file_local_copy
from computations import local_angle
from math import degrees
from inputParams import parameters
import numpy as np
import pandas as pd
import csv

Jt, Jf, Q, g, a0, v0, y0, xmax, tmax, h, dt, rounding_decimals = parameters.values()

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
    try:
        rk_X, rk_Y, U = rungekutta_main()
        kin_X, kin_Y = simulated_main()
    except Exception as e:
        print(f"An error ocurred calculating the curves with the initial conditions provided: {e}. "
              "Physically impossible initial conditions may cause some equations to break down. " 
              "Try different initial conditions.")
        exit()
    return {"rk4": [rk_X, rk_Y], "kinematics": [kin_X, kin_Y], "u_values": U}


def export_data(output_filename, file_format, data, vector_data):
    tang_norm_components = {}
    if vector_data:
        components_file_local_copy(data["u_values"], data["rk4"][1], data["rk4"][0])
        tang_norm_components = output_vector_data(data["rk4"][1], data["u_values"])

    if file_format == "xlsx":
        write_xlsx(output_filename, {**format_rk_data(data), **tang_norm_components})
    elif file_format == "csv":
        write_csv(output_filename, {**format_rk_data(data), **tang_norm_components})


def write_xlsx(filename, data):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)


def write_csv(filename, data):
    data_points = len(data["rk_X"])
    with open(filename, "w") as f:
        fieldnames = data.keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(data_points):
            row = {}
            for key, value in data.items():
                row[key] = round(value[i], rounding_decimals) # round to five decimal places
            writer.writerow(row)

def format_rk_data(data):
    angle_data = np.array([degrees(local_angle(u)) for u in data["u_values"]])
    result = {
        "rk_X": data["rk4"][0],
        "rk_y": data["rk4"][1],
        "U": data["u_values"],
        "angle": angle_data
    }
    return result


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


def output_vector_data(Y, U):
    data_points = len(Y)
    tang_accel, norm_accel, tang_jerk, norm_jerk = [np.empty(data_points) for _ in range(4)]
    for i in range(data_points):
        tang_accel[i] = tangential_accel2(U[i], Y[i])[1]
        norm_accel[i] = normal_accel2(U[i], Y[i])[1]
        tang_jerk[i] = tangential_jerk(U[i], Y[i])[1]
        norm_jerk[i] = normal_jerk(U[i], Y[i])[1]
    return {"tang_accel": tang_accel, "norm_accel": norm_accel, "tang_jerk": tang_jerk, "norm_jerk": norm_jerk}