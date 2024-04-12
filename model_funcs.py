import numpy as np

def line(x, *c):
    return c[0]*(x) + c[1]


def two_poly(x, *c):
    # Note that this parabola is in vertex form
    return c[0]*(x-c[1])**2 + c[2]


def three_poly(x, *c):
    return c[0]*(x)**3 + c[1]*(x)**2 + c[2]*(x) + c[3]


def four_poly(x, *c):
    return c[0]*(x)**4 + c[1]*(x)**3 + c[2]*(x)**2 + c[3]*(x) + c[4]


def five_poly(x, *c):
    return c[0]*(x)**5 + c[1]*(x)**4 + c[2]*(x)**3 + c[3]*(x)**2 + c[4]*(x) + c[5]


def six_poly(x, *c):
    return c[0]*(x)**6 + c[1]*(x)**5 + c[2]*(x)**4 + c[3]*(x)**3 + c[4]*(x)**2 + c[5]*(x) + c[6]


def seven_poly(x, *c):
    return c[0]*(x)**7 + c[1]*(x)**6 + c[2]*(x)**5 + c[3]*(x)**4 + c[4]*(x)**3 + c[5]*(x)**2 + c[6]*(x) + c[7]


def eight_poly(x, *c):
    return c[0]*(x)**8 + c[1]*(x)**7 + c[2]*(x)**6 + c[3]*(x)**5 + c[4]*(x)**4 + c[5]*(x)**3 + c[6]*(x)**2 + c[7]*(x) + c[8]


def nine_poly(x, *c):
    return c[0]*(x)**9 + c[1]*(x)**8 + c[2]*(x)**7 + c[3]*(x)**6 + c[4]*(x)**5 + c[5]*(x)**4 + c[6]*(x)**3 + c[7]*(x)**2 + c[8]*(x) + c[9]


def ten_poly(x, *c):
    return c[0]*(x)**10 + c[1]*(x)**9 + c[2]*(x)**8 + c[3]*(x)**7 + c[4]*(x)**6 + c[5]*(x)**5 + c[6]*(x)**4 + c[7]*(x)**3 + c[8]*(x)**2 + c[9]*(x) + c[10]


def ellipse(x, *c):
    return c[1]*(1 - ((x-c[2])/c[0])**2)**(1/2) + c[3]


# REMOVE EXPONENTIAL? It appears to simply be a poor way to model the surface; it grows too fast.
def exponential(x, *c):
    return c[0]*np.exp(c[1]*x - c[2]) + c[3]


models = {
        "line": line, "2_poly": two_poly, "3_poly": three_poly, "4_poly": four_poly, "5_poly": five_poly, 
        "6_poly": six_poly, "7_poly": seven_poly, "8_poly": eight_poly, "9_poly": nine_poly, "10_poly": ten_poly,
        "ellipse": ellipse, "exponential": exponential
        }