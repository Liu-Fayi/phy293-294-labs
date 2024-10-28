import tools as tl
import fit_black_box as bb
import numpy as np

def proportional(t, m):
    return m*t

l = 5.331677018579005e-07
l_err = 4.144240283077511e-09
L0 = 88.54 * 10**-3
L0_err = 0.01 * 10**-3
T0 = 21.6
T0_err = 0.1
T = np.array([21.6, 21.7, 21.8, 21.9, 22, 22.2, 22.3, 22.3, 22.6, 22.8, 22.9, 22.9, 23, 23.1, 23.4, 23.5,
              23.5, 23.6, 23.9, 24, 24.1, 24.1, 24.1, 24.2, 24.3, 24.5, 24.7, 24.7, 24.8, 25.1, 25.2, 25.3,
              25.4, 25.4, 25.5, 25.6, 25.8, 26, 26, 26.1, 26.2, 26.4, 26.6, 26.7, 26.7, 26.8, 26.9])
T_err = 0.1
dT = T - T0
dT_err = tl.error_add(T_err, T0_err)
N = np.array([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
              31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48])
N_err = 0.75

initial_guess = 8
bb.plot_fit(proportional, dT, N, dT_err, N_err, init_guess=initial_guess, font_size=20, xlabel="Temperature change (K)", ylabel="Number of fringes")

m_fit = 8.975206611178253
N_predicted = proportional(dT, m_fit)
m_fit_err = np.sqrt(len(dT) * ((1/(len(dT) - 2)) * np.sum((N - N_predicted) ** 2)) / (len(dT) * np.sum(dT**2) - np.sum(dT) ** 2))
print(f"m: {m_fit} +/- {m_fit_err}")
a = m_fit * l / 2 / L0
a_err = tl.error_mult(m_fit, l, m_fit_err, l_err, m_fit * l)
a_err = tl.error_mult(m_fit * l, 2, a_err, 0, m_fit * l / 2)
a_err = tl.error_mult(m_fit * l / 2, L0, a_err, L0_err, a)
print(f"coefficient of thermal expansion: {a} +/- {a_err}")


rmse = tl.rmse(N, N_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(N, N_predicted, N_err)
print(f"Chi squared: {chi2}")
red_chi2 = tl.reduced_chi_squared(chi2, 1, 47)
print(f"Reduced chi squared: {red_chi2}")
r2 = tl.r_sq(N, N_predicted)
print(f"R^2: {r2}")