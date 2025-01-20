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

r = np.array([15.825, 15, 14.6, 14.225, 13.3, 13, 12.5, 12.35, 11.95, 11.7, 11.5, 11.125])
V = np.array([2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8])
r = r / 1000
V = V * 1000
rerr = 0.0005
Verr = 100

log_V, log_r = tl.log_log(V, r)
log_Verr = tl.error_log(V, Verr, 10)
log_rerr = tl.error_log(r, rerr, 10)

initial_guess = [1, 1]
bb.plot_fit(linear, log_V, log_r, log_Verr, log_rerr, init_guess=initial_guess, font_size=20, xlabel="log(V)", ylabel="log(r)")

m_fit, m_fit_err = -0.5717114960163332, 0.015307489242173648
b_fit, b_fit_err = 0.34510471251841573, 0.12487732562755154