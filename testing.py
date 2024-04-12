import matplotlib.pyplot as plt
from sys import argv
import numpy as np
from scipy.optimize import curve_fit

params = [int(x) for x in argv[1:]]
print(params)

X = np.linspace(0, 100, 100)
Y = np.linspace(0, 100, 100)

def func1(x, *c):
    return c[0]*x**2 + c[1]*x + c[2]

popt, pcov = curve_fit(func1, X, Y, p0=params)
print(popt)


Y_reg = func1(X, *popt)

plt.plot(X, Y_reg)
plt.grid("both")
plt.ylim(0, 100)
plt.xlim(0, 100)
plt.show()