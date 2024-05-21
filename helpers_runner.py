from rungekutta import rungekutta_main
from simulated import simulated_main

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
