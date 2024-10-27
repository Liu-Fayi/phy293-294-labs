import tools as tl
import fit_black_box as bb
import numpy as np

def proportional(t, m):
    return m*t

dx = np.array([9, 11, 14, 5, 17, 19])
N = np.array([33, 43, 52, 18, 64, 71])
Nerr = np.array([1, 1, 1, 1, 1, 1])
dxerr = np.array([1, 1, 1, 1, 1, 1])

dx = dx / (10**6)
dxerr = dxerr / (10**6)

initial_guess = 3700000
bb.plot_fit(proportional, dx, N, dxerr, Nerr, init_guess=initial_guess, font_size=12, xlabel="Displacement (m)", ylabel="Number of fringes")

m_fit = 3751164.958099879
m_fit_err = 29157.296801090775

l = 2 / m_fit
l_err = tl.error_mult(m_fit, 2, m_fit_err, 0, l)
print(f"Lambda: {l} +/- {l_err}")

N_predicted = proportional(dx, m_fit)

rmse = tl.rmse(N, N_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(N, N_predicted, Nerr)
print(f"Chi squared: {chi2}")
red_chi2 = tl.reduced_chi_squared(chi2, 1, 6)
print(f"Reduced chi squared: {red_chi2}")
r2 = tl.r_sq(N, N_predicted)
print(f"R^2: {r2}")