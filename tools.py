import numpy as np

def error_add(da, db):
    return np.sqrt(da**2 + db**2)

def error_mult(a, b, da, db, sol):
    return sol * np.sqrt((da / a) ** 2 + (db / b) ** 2)

def error_exp(a, da, n, sol):
    return n * sol * (da/a)

def chi_squared(observed, predicted, uncertainty):
    return np.sum((observed - predicted)**2 / uncertainty**2)

def chi_squared_func(observed, independent, function, *params, uncertainty):
    return np.sum((observed - function(independent, *params))**2 / uncertainty**2)
