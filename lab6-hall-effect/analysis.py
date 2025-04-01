import tools
import fit_black_box as bb
import numpy as np
import math

# Define a linear model function
def linear(x, m, b):
    x = np.array(x)
    return x * m + b

# Dimensions 
width = 2.37e-3       # meters
width_err = 0.005e-3  # meters

# Calculate thickness 
seperation = (89.65E-3/8)  # meters
seperation_err = (0.005E-3)/8  # meters

step_size = 2.89E-3
step_size_err = 0.005E-3  # meters

thickness = step_size / seperation * 2945E-10 


thickness_err = tools.error_mult(step_size, seperation, step_size_err, seperation_err, sol=thickness)

thickness_err *= 2945E-10  

# Currents and voltages as dictionaries:
# Here the key (e.g., 1148) may represent the applied field (in mT) for which the measurements were made.
currents = {
    1148: [31.04, 24.57, 20.5, 14.95, 9.76],
    900: [29.96,24.88,20.22,14.63,9.75],  # in mA
    645: [30.22,24.88,20.22,14.63,9.75]
}

voltages = {
    1148: [0.0229, 0.0186, 0.0152, 0.0115, 0.0074],
    900: [0.0202,0.0162,0.0123,0.0081,0.004], # in mV
    645: [0.0136,0.0111,0.0085,0.0055,0.0028]
}

# Compute sheet current density Jx from currents (convert mA to A)
# Jx = I/(width*thickness)
Jx = {}
Jx_err = {}
for key in currents.keys():
    Jx[key] = [i * 1E-3 / (width * thickness) for i in currents[key]]
    Jx_err[key] = [tools.error_mult(width, thickness, width_err, thickness_err,
                                     sol=i * 1E-3 / (width * thickness))
                                     for i in currents[key]]

# Compute the transverse electric field, Ey
# Convert voltage from mV to V and divide by width.
E_y = {}
for key in voltages.keys():
    E_y[key] = [v * 1E-3 / width for v in voltages[key]]

# Propagate uncertainty in Ey (assume uncertainty in voltage is given via a fixed value, here 0.00035E-3 for example)
E_y_err = {}
for key in voltages.keys():
    E_y_err[key] = [tools.error_mult(v * 1E-3, width, 0.0002E-3, width_err,
                                     sol=v * 1E-3 / width)
                                     for v in voltages[key]]

# Perform fits and compute chi-squared values for each applied field:
m = {}
chi2 = {}
red_chi2 = {}
rmse = {}
r2 = {}
for key in voltages.keys():
    popt, perr = bb.plot_fit(linear, Jx[key], E_y[key], Jx_err[key], E_y_err[key],
                             init_guess=[1E-11, 0], 
                             xlabel="Jx (A/m^2)",
                             ylabel="Ey (V/m)",
                             filename="graph" + str(key) + ".png")
    m[key] = popt  # popt contains [m, b]
    
    pred = linear(Jx[key], m[key][0], m[key][1])
    chi2[key] = tools.chi_squared(np.array(E_y[key]), pred, np.array(E_y_err[key]))
    # Degrees of freedom = (number of data points) - (number of fitted parameters)
    red_chi2[key] = tools.reduced_chi_squared(chi2[key], 2, len(Jx[key]) )
    rmse[key] = tools.rmse(np.array(E_y[key]), pred)
    #r squared
    r2[key] = tools.r_sq(np.array(E_y[key]), pred)
    print(f"For applied field {key} mT:")
    print(f"    Best fit m = {m[key][0]:.3e} +/- {perr[0]:.3e} V m/A")
    print(f"    Chi squared: {chi2[key]:.2f}")
    print(f"    Reduced chi squared: {red_chi2[key]:.2f}")
    print(f"    RMSE: {rmse[key]:.3e} V/m")
    print(f"    R^2: {r2[key]:.3f}")


# Calculate Rh for each applied field (key assumed in mT; convert to T)
Rh = []
for key in voltages.keys():
    Rh_value = m[key][0] / (key * 1E-3) 
    Rh.append(Rh_value)
    print(f"Rh for {key} mT: {Rh_value:.3e} m^3/C")

# Average Rh and compute standard error of the mean
Rh_mean = np.mean(Rh)
Rh_std = np.std(Rh, ddof=1) / np.sqrt(len(Rh))
print(f"Average Rh: {Rh_mean:.3e} +/- {Rh_std:.3e} m^3/C")

lit_rh = 8.9E-11  # m^3/C

# Calculate percent difference between average Rh and literature value
percent_diff = 100 * abs(Rh_mean - lit_rh) / lit_rh
print(f"Percent difference: {percent_diff:.2f}%")

# Calculate percent error in Rh
percent_error = 100 * Rh_std / Rh_mean
print(f"Percent error: {percent_error:.2f}%")

