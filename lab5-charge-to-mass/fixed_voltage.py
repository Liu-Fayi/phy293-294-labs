import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.0326

n = 130
def inverse(t, a,b):
    return a/t+b
def linear(t, a,b):
    return a*t+b

i = np.array([1.010,1.081,1.206,1.334,1.499,1.624])
r = np.array([0.059,0.055,0.05,0.045,0.04,0.037])

v = 186.01

b_c = [((4/5)**(3/2))* (mue_0*n)/R * i for i in i]


inital_guess = [1,1]
bb.plot_fit(inverse, i, r, init_guess=inital_guess, font_size=20, xlabel="Current (A)", ylabel="Radius (m)")

a_fit,a_fit_unc = 0.05866058897786993, 0.000736254011077414
b_fit,b_fit_unc = 0.0009644696309139551, 0.0005943279413311962

rmse = tl.rmse(r, inverse(i, a_fit,b_fit))
print(f"RMSE: {rmse}")

chi_squared = tl.chi_squared(r, inverse(i, a_fit,b_fit), 0.0002)
print(f"Chi squared: {chi_squared}")

reduced_chi_squared = tl.reduced_chi_squared(chi_squared, 2, 6)
print(f"Reduced chi squared: {reduced_chi_squared}")


######## B calculation ########

inital_guess = [1,1]
# fit B_c to a linear function of 1/r
bb.plot_fit(linear, 1/r, b_c, init_guess=inital_guess, font_size=20, xlabel="1/Radius (1/m)", ylabel="B_c (T)")

