import tools
import fit_black_box as bb
import numpy as np
import math

# Define a linear model function
def linear(x, m,b):
    x = np.array(x)
    return x * m + b

# Dimensions 
width = 16.25e-2     # meters
width_err = 0.005e-2 # meters

# Calculate thickness 
thickness = (2 / 26.15e-2) * 2945E-10   # meters
thickness_err = tools.error_mult(2945E-10, 2 / 26.15e-2, 0, 0.005e-2, sol=thickness)

# Currents and voltages 
currents = [9.93, 14.96, 19.98, 24.97, 29.95]  # in mA

voltages = {
    569: [0.0073,0.0089,0.0096,0.011,0.0111],  # in mV
    961: [0.01,0.0127,0.0146,0.0174,0.0189],
    1136: [0.0109,0.0143,0.0168,0.0198,0.0223]
}

# Compute sheet current density Jx from currents (convert mA to A)
Jx = [i * 1E-3 / (width * thickness) for i in currents]
Jx_err = [tools.error_mult(width, thickness, width_err, thickness_err, sol=i * 1E-3 / (width * thickness)) for i in currents]

# Compute the transverse electric field, Ey
E_y = {}
for key in voltages.keys():
    E_y[key] = [v * 1E-3 / width for v in voltages[key]]

# Propagate uncertainty in Ey
E_y_err = {}
for key in voltages.keys():
    E_y_err[key] = [tools.error_mult(v * 1E-3, width, 0.00035E-3, width_err, sol=v * 1E-3 / width) for v in voltages[key]]

m = {}
chi2 = {}
red_chi2 = {}
for key in voltages.keys():
    popt, perr = bb.plot_fit(linear, Jx, E_y[key], Jx_err, E_y_err[key],
                             init_guess=[1E-11,0], 
                             xlabel="Jx (A/m^2)",
                             ylabel="Ey (V/m)",
                             filename="graph" + str(key) + ".png")
    m[key] = popt

    pred = linear(Jx, m[key][0], m[key][1])
    chi2[key] = tools.chi_squared(np.array(E_y[key]), pred, np.array(E_y_err[key]))
    red_chi2[key] = tools.reduced_chi_squared(chi2[key], 1, len(Jx) - 1)
    print(f"For applied field {key} mT:")
    print(f"    Best fit m = {m[key][0]:.3e} +/- {perr[0]:.3e} V m/A")
    print(f"    Chi squared: {chi2[key]:.2f}")
    print(f"    Reduced chi squared: {red_chi2[key]:.2f}")

# Calculate Rh
Rh = []
for key in voltages.keys():
    Rh_value = m[key][0] / (key * 10**-3)  # Convert key from mT to T
    Rh.append(Rh_value)
    print(f"Rh for {key} mT: {Rh_value:.3e} m^3/C")
# Average Rh and compute uncertainty
Rh_mean = np.mean(Rh)
Rh_std = np.std(Rh, ddof=1) / np.sqrt(len(Rh))  # Standard error of the mean
print(f"Average Rh: {Rh_mean:.3e} +/- {Rh_std:.3e} m^3/C")