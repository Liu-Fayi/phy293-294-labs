import math

import tools as tl
import fit_black_box as bb
import numpy as np

h = 6.62607015e-34
R = 0.065
n = 1
m = 9.10938356e-31
e = 1.60217662e-19

def linear(t, a, b):
    return a*t + b

def power(t, a, b):
    return a*t**b

def proportional(t, m):
    return m*t

r = np.array([15.825, 15, 14.6, 14.225, 13.3, 13, 12.5, 12.35, 11.95, 11.7, 11.5, 11.125])
V = np.array([2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8])
r = r / 1000
V = V * 1000
rerr = 0.2/1000
Verr = 100

log_V, log_r = tl.log_log(V, r)
log_Verr = tl.error_log(V, Verr, math.e)
log_rerr = tl.error_log(r, rerr, math.e)

initial_guess = [1, 1]
bb.plot_fit(linear, log_V, log_r, log_Verr, log_rerr, init_guess=initial_guess, font_size=20, xlabel="log(Voltage)", ylabel="log(radius)")
# bb.plot_fit(power, V, r, Verr, rerr, init_guess=initial_guess, font_size=20, xlabel="V", ylabel="r")

m_fit, m_fit_err = -0.5717114431915732, 0.015307491587896769
b_fit, b_fit_err = 0.34510428139650384, 0.1248773416094752

coeff = np.exp(b_fit)
coeff_err = tl.error_exp2(math.e, b_fit, b_fit_err)
d = 2*R*n*h/(np.sqrt(2*m*e)*coeff)
d_err = tl.error_exp(coeff, coeff_err, -0.5, 1/coeff**0.5)
d_err = tl.error_mult(1/coeff**0.5, 2*R*n*h/(np.sqrt(2*m*e)), d_err, 0, b)
print(f"b: {d} +/- {d_err}")

log_r_predicted = linear(log_V, m_fit, b_fit)

rmse = tl.rmse(log_r, log_r_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(log_r, log_r_predicted, log_rerr)
print(f"Chi squared: {chi2}")

red_chi2 = tl.reduced_chi_squared(chi2, 2, 12)
print(f"Reduced chi squared: {red_chi2}")

r2 = tl.r_sq(log_r, log_r_predicted)
print(f"R^2: {r2}")