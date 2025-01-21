import math

import tools as tl
import fit_black_box as bb
import numpy as np

h = 6.62607015e-34
R = 0.065
n = 1
m = 9.10938356e-31
e = 1.60217662e-19

def proportional(t, m):
    return m*t

r = np.array([27.2215579, 25.41957937, 24.97181917, 24.29529362, 22.78981911, 22.2693393, 21.4613737, 21.06880229, 20.48782254, 20.11216961, 19.7523267, 19.26106641])
V = np.array([2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8])
r = r / 1000
V = V * 1000
rerr = 0.2/1000
Verr = 100


lam = h / (np.sqrt(2*m*e*V))
lam_err = tl.error_mult(V, 2*m*e, Verr, 0, V*2*m*e)
lam_err = tl.error_exp(2*m*e*V, lam_err, -0.5, 1/np.sqrt(2*m*e*V))
lam_err = tl.error_mult(1/np.sqrt(2*m*e*V), h, lam_err, 0, lam)


bb.plot_fit(proportional, lam, r, lam_err, rerr, font_size=20, xlabel="Wavelength (m)", ylabel="Radius (m)")

m_fit = 641291494.7007778
m_fit_err = 3233288.4802381983

d = 2 * R * n / m_fit
d_err = tl.error_mult(m_fit, 2, m_fit_err, 0, d)
print(f"d: {d} +/- {d_err}")

r_predicted = proportional(lam, m_fit)

rmse = tl.rmse(r, r_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(r, r_predicted, rerr)
print(f"Chi squared: {chi2}")

red_chi2 = tl.reduced_chi_squared(chi2, 1, 12)
print(f"Reduced chi squared: {red_chi2}")

r2 = tl.r_sq(r, r_predicted)
print(f"R^2: {r2}")