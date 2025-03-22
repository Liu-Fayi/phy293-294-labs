import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.326/2
R_err = .5/2000

n = 130

def linear(t, a,b):
    return a*t+b

i = np.array([1.010,1.081,1.206,1.334,1.499,1.624])
r = np.array([0.059,0.055,0.05,0.045,0.04,0.037])

r_err = [0.5/2000]*6
i_err = [0.001]*6
v = 186.01

b_c = [((4/5)**(3/2)) * (mue_0*n*i)/R  for i in i]
b_c_err = [tl.error_mult(current, R, current_err, R_err, bc) for current, current_err, bc in zip(i, i_err, b_c)]
print(b_c[0],b_c_err[0])

#correct for the non-uniformity of the magnetic field
b_c = [b*(1-(r**4/(R**4*(0.6583+0.29*(r**2/R**2))**2))) for b,r in zip(b_c,r)]
# Calculate error propagation for the magnetic field correction
correction_errors = []
for b, b_err, r_val, r_error in zip(b_c, b_c_err, r, r_err):
    # Define correction factor terms for clarity
    r4 = r_val**4
    R4 = R**4
    r2_R2 = (r_val**2)/(R**2)
    denom = (0.6583 + 0.29*r2_R2)**2
    
    # Partial derivatives
    db = (1 - r4/(R4*denom))
    dr = b*(-4*r_val**3/(R4*denom) + 2*r4*0.29/(R4*denom**2 * R**2))
    
    # Combine errors using quadrature
    total_error = np.sqrt((db*b_err)**2 + (dr*r_error)**2)
    correction_errors.append(total_error)

b_c_err = correction_errors

  
inital_guess = [1,1]
# fit B_c to a linear function of 1/r
fit, unc = bb.plot_fit(linear, 1/r, b_c, init_guess=inital_guess, font_size=20, xlabel="1/Radius (1/m)", ylabel="B_c (T)", xerror=[0.5/2000]*6,yerror=b_c_err,filename="extra_field_fit.png")

alpha_fit, b_e = fit
alpha_err, b_e_err = unc


rmse = tl.rmse(b_c, linear(1/r, alpha_fit,b_e))
print(f"RMSE: {rmse}")

chi_squared = tl.chi_squared(b_c, linear(1/r, alpha_fit,b_e), np.array(b_c_err))
print(f"Chi squared: {chi_squared}")

reduced_chi_squared = tl.reduced_chi_squared(chi_squared, 2, 6)
print(f"Reduced chi squared: {reduced_chi_squared}")




print(tl.r_sq(b_c, linear(1/r, alpha_fit,b_e)))