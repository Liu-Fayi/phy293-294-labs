import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.0326
R_err = .5/2000
n = 130

b_e,b_e_unc = -7.150239265774714*10**-5, 0.00014976036350813733

k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R

I_o = b_e/k
I_0_err = tl.error_mult(b_e, k, b_e_unc, 0, I_o)

##calculation of constant with fixed current fit
i = 1.076
a,a_err = 0.004006761994633504, 0.00004674028226632868
e_ratio_I = 1/((a*k)*(i+1/math.sqrt(2)*I_o))**2

e_ratio_I_err = tl.error_mult(a*k, i+1/math.sqrt(2)*I_o, a_err, I_0_err, e_ratio_I)

print(e_ratio_I, e_ratio_I_err)

##calculation of constant with fixed voltage fit
v = 186.01
a_fit,a_fit_unc = 0.05866058897786993, 0.000736254011077414
b_fit,b_fit_unc = 0.02821757154659192, 0.015467814817588977

e_ratio_V = v/(a_fit*k)**2

print(e_ratio_V)

#compare to the accepted value
accepted = 1.758820024*10**11

#percent error
percent_error_I = abs(e_ratio_I - accepted)/accepted
percent_error_V = abs(e_ratio_V - accepted)/accepted
#in percent
percent_error_I *= 100
percent_error_V *= 100

print(f"Percent error for fixed current fit: {percent_error_I}")
print(f"Percent error for fixed voltage fit: {percent_error_V}")



