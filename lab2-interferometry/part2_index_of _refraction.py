import tools as tl
import fit_black_box as bb
import numpy as np

def quadratic_proportional(t, a):
    return a*t**2

t = 7.77 / 1000
t_err = 0.01 / 1000
l = 5.331677018579005e-07
l_err = 4.144240283077511e-09
theta_f = np.array([73.66666667, 69.41666667, 69, 71, 71.83333333, 70])
theta_i = np.array([73.66666667, 73.66666667, 73.66666667, 73.66666667, 73.66666667, 73.66666667])
theta_err = np.array([0.25/6, 0.25/6, 0.25/6, 0.25/6, 0.25/6, 0.25/6])
dtheta = (theta_i - theta_f) / 180 * np.pi
dtheta_err = (tl.error_add(theta_err, theta_err) / 180) * np.pi
N = np.array([0, 28, 32, 11, 5, 20])
N_err = 0.75

initial_guess = 1
bb.plot_fit(quadratic_proportional, dtheta, N, dtheta_err, N_err, init_guess=initial_guess, font_size=20, xlabel="Angle (rad)", ylabel="Number of fringes")

a_fit = 4930.000705260947
N_predicted = quadratic_proportional(dtheta, a_fit)
a_fit_err = np.sqrt(len(dtheta) * ((1/(len(dtheta) - 2)) * np.sum((N - N_predicted) ** 2)) / (len(dtheta) * np.sum(dtheta**4) - np.sum(dtheta**2) ** 2))

n = 1 / (1 - (l * a_fit) / t)
n_err = tl.error_mult(l, a_fit, l_err, a_fit_err, l * a_fit)
n_err = tl.error_mult(l * a_fit, t, n_err, t_err, l * a_fit / t)
n_err = tl.error_add(0, n_err)
n_err = tl.error_mult(1 - (l * a_fit) / t, 1, n_err, 0, n)
print(f"Index of refraction: {n} +/- {n_err}")

rmse = tl.rmse(N, N_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(N, N_predicted, N_err)
print(f"Chi squared: {chi2}")
red_chi2 = tl.reduced_chi_squared(chi2, 1, 6)
print(f"Reduced chi squared: {red_chi2}")
r2 = tl.r_sq(N, N_predicted)
print(f"R^2: {r2}")