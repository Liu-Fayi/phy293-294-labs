import math
from math import log10

import numpy as np

def error_add(da, db):
    return np.sqrt(da**2 + db**2)

def error_mult(a, b, da, db, sol):
    return sol * np.sqrt((da / a) ** 2 + (db / b) ** 2)

def error_exp(a, da, n, sol):
    return n * sol * (da/a)

def error_log(a, da, base):
    return log10(math.e) / log10(base) * (da/a)

def chi_squared(observed, predicted, uncertainty):
    return np.sum((observed - predicted)**2 / uncertainty**2)

def chi_squared_func(observed, independent, function, *params, uncertainty):
    return np.sum((observed - function(independent, *params))**2 / uncertainty**2)

def reduced_chi_squared(chi2, parameters, data_points):
    return chi2 / (data_points - parameters)

def rmse(observed, predicted):
    return np.sqrt(np.mean((observed - predicted) ** 2))

def r_sq(observed, predicted):
    return 1 - np.sum((observed - predicted)**2) / np.sum((observed - np.mean(observed))**2)