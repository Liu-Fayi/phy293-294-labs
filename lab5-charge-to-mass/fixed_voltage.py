import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.326/2
v = 186.01
n = 130
b_e,b_e_unc = 6.85323006340271*10**-5, 1.2710535253099034*10**-5
k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R
I_o = b_e/k



def inverse(t, a,):
    return a*math.sqrt(v)/(t+1/math.sqrt(2)*I_o) 

i = np.array([1.010,1.081,1.206,1.334,1.499,1.624])
r = np.array([0.059,0.055,0.05,0.045,0.04,0.037])

v = 186.01


inital_guess = [1]
bb.plot_fit(inverse, i, r, init_guess=inital_guess, font_size=20, xlabel="Current (A)", ylabel="Radius (m)", xerror=[0.001]*6, yerror=[0.0005/2]*6, filename="fixed_current_fit.png")

a_fit,a_fit_unc = 0.004738608386267347, 1.8655570064236386 * 10**-5

rmse = tl.rmse(r, inverse(i, a_fit))
print(f"RMSE: {rmse}")

chi_squared = tl.chi_squared(r, inverse(i, a_fit), 0.0005/2)
print(f"Chi squared: {chi_squared}")

reduced_chi_squared = tl.reduced_chi_squared(chi_squared, 1, 6)
print(f"Reduced chi squared: {reduced_chi_squared}")

