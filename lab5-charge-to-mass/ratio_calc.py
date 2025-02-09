import math

import tools as tl
import fit_black_box as bb
import numpy as np

mue_0 = 4 * math.pi * 10**-7
R = 0.326/2
R_err = 0.005/2
n = 130

b_e,b_e_unc = 6.85323006340271*10**-5, 1.2710535253099034*10**-5
k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R
k_err = tl.error_mult(1/math.sqrt(2), (4/5)**(3/2) * mue_0 * n / R, 0, R_err, k)
I_o = b_e/k
I_o_err = tl.error_mult(b_e, k, b_e_unc, k_err, I_o)

##calculation of constant with fixed current fit
i = 1.076
a,a_err = 0.004006761994742138, 4.674028233227996*10**-5
e_ratio_I = 1/((a*k)*(i+1/math.sqrt(2)*I_o))**2
e_ratio_I_err = tl.error_mult(i, a*k, 0.001, a_err, e_ratio_I)

print(f"Fixed current fit: {e_ratio_I} +/- {e_ratio_I_err}")

##calculation of constant with fixed voltage fit
v = 186.01
a_fit,a_fit_unc = 0.004738608386267347, 0.0007849603700117398
b_fit,b_fit_unc = 0.028217571546591925, 0.015467814817588977

e_ratio_V = 1/(a_fit*k)**2
e_ratio_V_err = tl.error_mult(v, a_fit*k, 0.01, a_fit_unc, e_ratio_V)

print(f"Fixed voltage fit: {e_ratio_V} +/- {e_ratio_V_err}")

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

#avg and std dev
avg = (e_ratio_I + e_ratio_V)/2
avg_err = math.sqrt(e_ratio_I_err**2 + e_ratio_V_err**2)/2

print(f"Average: {avg} +/- {avg_err}")

percent_error_avg = abs(avg - accepted)/accepted
percent_error_avg *= 100
print(f"Percent error for average: {percent_error_avg}")



