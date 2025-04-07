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
seperation = (12.5E-3)  # meters
seperation_err = (0.005E-3)  # meters

step_size = 1.28E-3
step_size_err = 0.005E-3  # meters

thickness = step_size / seperation * 2945E-10 


thickness_err = tools.error_mult(step_size, seperation, step_size_err, seperation_err, sol=thickness)

thickness_err *= 2945E-10  

print(f"Thickness: {thickness:.3e} +/- {thickness_err:.3e} m")

# Currents and voltages as dictionaries:
# Here the key (e.g., 1148) may represent the applied field (in mT) for which the measurements were made.
currents = {
    1148: [31.04, 24.57, 20.5, 14.95, 9.76],
    900: [29.96,24.88,20.22,14.63,9.75],  # in mA
    645: [30.22,24.88,20.22,14.63,9.75],
    330: [29.63,25.19,20.15,15.22]
}
curr_unc = 0.01E-3  #A
vol_unc = 0.0002E-3  #V

voltages = {
    1148: [0.0229, 0.0186, 0.0152, 0.0115, 0.0074],
    900: [0.0202,0.0162,0.0123,0.0081,0.004], # in mV
    645: [0.0136,0.0111,0.0085,0.0055,0.0028],
    330:[0.006,0.0047,0.0032,0.0015]
}

# Compute sheet current density Jx from currents (convert mA to A)
# Jx = I/(width*thickness)
Jx = {}
Jx_err = {}
for key in currents.keys():
    Jx[key] = [i * 1E-3 / (width * thickness) for i in currents[key]]
    w_t_err = tools.error_mult(width, thickness, width_err, thickness_err,
                                sol=width * thickness)
    
    Jx_err[key] = [tools.error_mult(i * 1E-3, width*thickness, curr_unc, w_t_err,
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
    E_y_err[key] = [tools.error_mult(v * 1E-3, width, vol_unc, width_err,
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
key_unc = 0.001E-3  # mT to T conversion factor
for key in voltages.keys():
    Rh_value = m[key][0] / (key * 1E-3) 
    Rh.append(Rh_value)
    Rh_err = tools.error_mult(m[key][0], key * 1E-3, perr[0], key_unc,
                               sol=m[key][0] / (key * 1E-3))
    print(f"Rh for {key} mT: {Rh_value:.3e} +/- {Rh_err:.3e} m^3/C")
    # Propagate uncertainty in Rh


# Average Rh and compute standard error of the mean
Rh_mean = np.mean(Rh)
#weighted average of the errors
Rh_std = np.sqrt(np.sum([(i - Rh_mean)**2 for i in Rh]) / (len(Rh) - 1))
Rh_std /= np.sqrt(len(Rh))  # Standard error of the mean

print(f"Average Rh: {Rh_mean:.3e} +/- {Rh_std:.3e} m^3/C")

lit_rh = 8.9E-11  # m^3/C

# Calculate percent difference between average Rh and literature value
percent_diff = 100 * abs(Rh_mean - lit_rh) / lit_rh
print(f"Percent difference: {percent_diff:.2f}%")

# Calculate percent error in Rh
percent_error = 100 * Rh_std / Rh_mean
print(f"Percent error: {percent_error:.2f}%")


resistance = 0.9424  # Ohms
resistance_err = 0.0001
#calculate the resistivity
#resistance is in Ohms, width and thickness are in meters, 
resistivity = resistance * (width * thickness)/ 16.25E-3 
resistivity_err = tools.error_mult(resistance, width * thickness, resistance_err, width_err * thickness,
                                    sol=resistance * (width * thickness)/ 16.25E-3)

resistivity_err /= 16.25E-3  

print(resistivity)
print(resistivity_err)


number_density = 1/(Rh_mean * 1.6E-19) 
number_density_err = tools.error_mult(Rh_mean, 1.6E-19, Rh_std, 0.0001E-19,
                                        sol=Rh_mean / (1.6E-19))

print(f"Number density: {number_density:.3e} +/- {number_density_err:.3e} m^-3")

#drift velocity at 29.96 mA

current_dens = Jx[330][0]
current_dens_err = Jx_err[330][0]

drift_velocity = current_dens / (number_density * 1.6E-19)  # m/s
drift_velocity_err = tools.error_mult(current_dens, number_density * 1.6E-19, current_dens_err, number_density_err * 1.6E-19,
                                        sol=current_dens / (number_density * 1.6E-19))

print(f"Drift velocity: {drift_velocity:.3e} +/- {drift_velocity_err:.3e} m/s")

#conductive_mob = drift_velocity/E where E = IR/L 

E_applied = 29.96E-3 * resistance / 0.00237  # V/m

E_applied_err = tools.error_mult(29.96E-3, resistance, 0.001E-3, resistance_err,
                                  sol=29.96E-3 * resistance / 0.00237) / 0.00237

print(f"Applied electric field: {E_applied:.3e} +/- {E_applied_err:.3e} V/m")

conductive_mob = drift_velocity / E_applied  # m^2/Vs   

conductive_mob_err = tools.error_mult(drift_velocity, E_applied, drift_velocity_err, E_applied_err,
                                      sol=drift_velocity / E_applied)
print(f"Conductive mobility: {conductive_mob:.3e} +/- {conductive_mob_err:.3e} m^2/Vs")



