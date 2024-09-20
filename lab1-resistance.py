import fit_black_box as bb

# First, define the function you want to fit. Here it's a linear function.
# It is critical that the independant variable ("t") is first in the list of function variables.

def linear(t, m, b):
    return m*t + b

v1 = bb.np.array([6.499,6.500,6.502,6.502])
i1 = bb.np.array([62.88,29.987,13.939,2.413])
verr1 = bb.np.array([0.0052495,0.0053,0.005251,0.005251])
ierr1 = bb.np.array([0.13076,0.065,0.032878,0.009826])


v2 = bb.np.array([6.387,6.448
,6.477
,6.498])
i2 = bb.np.array([62.91,30.006,13.942,2.414])
verr2 = bb.np.array([0.00531935,0.0053224,0.00532385,0.0053249])
ierr2 = bb.np.array([0.062582,0.0560012,0.0077884,0.0054828])

init_guess = (-0.5, 0) # guess for the best fit parameters
font_size = 12
xlabel = "Voltage (V)"
ylabel = "Current (A)"

# Now we make the plot, displayed on screen and saved in the directory, and print the best fit values
bb.plot_fit(linear, i1, v1, ierr1, verr1, init_guess=init_guess, font_size=font_size,
            xlabel=xlabel, ylabel=ylabel)
bb.plot_fit(linear, i2,v2, ierr2, verr2, init_guess=init_guess, font_size=font_size,
            xlabel=xlabel, ylabel=ylabel)