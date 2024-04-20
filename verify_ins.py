# verify inputs for curve-fitting
def curve_fit_ins(model, params):

    params = [float(x) for x in params.split(",")]
    if len(model.split("_")) == 2 and model.split("_")[1] == "poly":
        deg = int(model.split("_")[0])
        if deg > 10: 
            exit(f"A {deg}-degree polynomial model is not available. You must implement it in the source code.")
        if len(params) - 1 != deg:
            exit(f"This polynomial takes in {deg+1} parameters, not {len(params)}.")
    elif model == "line" and len(params) != 2:
        exit(f"The linear model only accepts 2 initial parameters, not {len(params)}.")
    elif model == "ellipse" and len(params) != 4:
        exit(f"The elliptical model only accepts 4 parameters, not {len(params)}.")
    elif model == "exponential" and len(params) != 4:
        exit(f"The exponential model only accepts 4 parameters, not {len(params)}.")

    return True


# verify inputs for hodograph
def hodograph_ins(argv):

    if argv[1] not in ["jerk", "jerk_comp", "jerk_tan_norm", "accel", "accel_comp", "accel_tan_norm"]:
        exit("To display a hodograph, you must select one of the following as the second CLA: " 
             "'jerk', 'jerk_comp', 'jerk_tan_norm', 'accel', 'accel_comp', or 'accel_tan_norm'. ")
    try:
        int(argv[2])
        float(argv[3])
    except:
        exit("One of your inputs for the number of frames or pause length is invalid.")
    
    if float(argv[3]) >= 1:
            exit("Pause length (fourth CLA) must be floating-point value less than 1.")

    return True, int(argv[2]), float(argv[3])


# verify inputs for view functionality
def view_ins(argv):
    if len(argv) == 5: bounds = argv[4].split(",")
    elif len(argv) == 3: bounds = argv[2].split(",")

    bounds = [int(x) for x in bounds]
    if bounds[0] < bounds[1] and bounds[2] < bounds[3]:
        return bounds, True
    else:
        exit("Bounds are incorrect. Accepted format is x1,x2,y1,y2 where x1 and y1 must "
             "be less than x2 and y2, respectively.")
