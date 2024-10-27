import tools as tl
import fit_black_box as bb
import numpy as np

def proportional(t, m):
    return m*t

half_coherence_length = (23-14) * (10**-6)
half_coherence_length_err = 0.5 * (10**-6)
half_coherence_N = 24
half_coherence_N_err = 1

coherence_length = half_coherence_length * 2
coherence_length_err = tl.error_mult(half_coherence_length, 2, half_coherence_length_err, 0, coherence_length)
coherence_N = half_coherence_N * 2
coherence_N_err = tl.error_mult(half_coherence_N, 2, half_coherence_N_err, 0, coherence_N)
print(f"Coherence length distance: {coherence_length} +/- {coherence_length_err}")
print(f"Coherence length wave count: {coherence_N} +/- {coherence_N_err}")

dx = np.array([9, 4, 7, 12])
N = np.array([24, 13, 20, 30,])
Nerr = np.array([1, 1, 1, 1])
dxerr = np.array([1, 1, 1, 1])

dx = dx / (10**6)
dxerr = dxerr / (10**6)

initial_guess = 2648275.861687403
bb.plot_fit(proportional, dx, N, dxerr, Nerr, init_guess=initial_guess, font_size=12, xlabel="Displacement (m)", ylabel="Number of fringes")

m_fit, m_fit_err = 2648275.861687403, 113076.81171228216
l = 2 / m_fit
l_err = tl.error_mult(m_fit, 2, m_fit_err, 0, l)
print(f"Lambda: {l} +/- {l_err}")

N_predicted = proportional(dx, m_fit)

rmse = tl.rmse(N, N_predicted)
print(f"RMSE: {rmse}")

chi2 = tl.chi_squared(N, N_predicted, Nerr)
print(f"Chi squared: {chi2}")
red_chi2 = tl.reduced_chi_squared(chi2, 1, 4)
print(f"Reduced chi squared: {red_chi2}")
r2 = tl.r_sq(N, N_predicted)
print(f"R^2: {r2}")