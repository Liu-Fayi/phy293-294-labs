import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.326/2
v = 186.01
n = 130
R_err = .5/2000
b_e, b_e_unc = 7.279481489311506e-5, 1.313424340798893e-5 
k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R
k_err = k * (R_err/R)

# Calculate I_o = b_e/k with standard propagation for a quotient:

I_o = b_e/k
I_o_err = I_o * np.sqrt((b_e_unc/b_e)**2 + (k_err/k)**2)

print("I_o: ", I_o, "+/-", I_o_err) 

def inverse(t, a, I_o):
    return a/(t+1/math.sqrt(2)*I_o) 

i = np.array([1.010,1.081,1.206,1.334,1.499,1.624])
r = np.array([0.059,0.055,0.05,0.045,0.04,0.037])

v = 186.01


inital_guess = [1,I_o]
fit, unc = bb.plot_fit(inverse, i, r, init_guess=inital_guess, font_size=20, xlabel="Current (A)", ylabel="Radius (m)", xerror=[0.001]*6, yerror=[0.0005]*6, filename="fixed_voltage_fit.png",bounded=True,bounds=([-np.inf,I_o-I_o_err],[+np.inf,I_o+I_o_err]))

a_fit, I_o = fit
a_fit_err, I_o_err = unc

rmse = tl.rmse(r, inverse(i, a_fit, I_o))
print(f"RMSE: {rmse}")

chi_squared = tl.chi_squared(r, inverse(i, a_fit,I_o), 0.0005)
print(f"Chi squared: {chi_squared}")

reduced_chi_squared = tl.reduced_chi_squared(chi_squared, 2, 6)
print(f"Reduced chi squared: {reduced_chi_squared}")


