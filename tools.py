import numpy as np

def error_add(da, db):
    return np.sqrt(da**2 + db**2)

def error_mult(a, b, da, db, sol):
    return sol * np.sqrt((da / a) ** 2 + (db / b) ** 2)

def error_exp(a, da, n, sol):
    return n * sol * (da/a)

