import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.326/2
n = 130
i = 1.076

B_c = (4/5)**(3/2) * mue_0 * n * i / R

k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R



def fit_function(delta_v, a):
    return a * np.sqrt(delta_v)

v = np.array([216.99, 188,151.99, 122.99,100.97,88.96])
r = np.array([0.06,0.055,0.05,0.045,0.04,0.035])
i = 1.076
v_err = [0.01]*6
r_err = [0.5/2000]*6





initial_guess = [1]
bb.plot_fit(fit_function,v,r,v_err,r_err, init_guess=initial_guess, font_size=20, xlabel="Voltage (V)", ylabel="Radius (m)")

a_fit = 0.004006761994633504
a_fit_err = .00004674028226632868

rmse = tl.rmse(r, fit_function(v, a_fit))
print(f"RMSE: {rmse}")

chi_squared = tl.chi_squared(r, fit_function(v, a_fit), 0.5/2000)
print(f"Chi squared: {chi_squared}")

reduced_chi_squared = tl.reduced_chi_squared(chi_squared, 1, 6)
print(f"Reduced chi squared: {reduced_chi_squared}")





