import fit_black_box as bb
import tools as tl
import numpy as np

# First, define the function you want to fit. Here it's a linear function.
# It is critical that the independant variable ("t") is first in the list of function variables.

def linear(t, m, b):
    return m*t + b

def rmse(observed, predicted):
    return np.sqrt(np.mean((observed - predicted) ** 2))

r = bb.np.array([101.54,214.94,464.8,2694.3])
rerr = bb.np.array([0.25,0.48,1.4,5.9])
v1 = bb.np.array([6.499,6.500,6.502,6.502])
i1 = bb.np.array([62.88,29.987,13.939,2.413])
verr1 = bb.np.array([0.0052495,0.0053,0.005251,0.005251])
ierr1 = bb.np.array([0.13076,0.065,0.032878,0.009826])
i1 = i1/1000
ierr1 = ierr1/1000
err1 = []

m_fit1, b_fit1 = -0.05410673394399822, 6.5022301915876435   
m_fit2, b_fit2 = -1.835005967853445, 6.502628691816137

v2 = bb.np.array([6.387,6.448,6.477,6.498])
i2 = bb.np.array([62.91,30.006,13.942,2.414])
verr2 = bb.np.array([0.00531935,0.0053224,0.00532385,0.0053249])
ierr2 = bb.np.array([0.062582,0.0560012,0.0077884,0.0054828])

finals = []
for i in range(len(r)):
    ra = tl.error_mult(r[i], i1[i], rerr[i], ierr1[i], r[i]*i1[i])
    b = tl.error_add(verr1[i], ra)
    c = tl.error_mult(i1[i], v1[i]-(r[i]*i1[i]), ierr1[i], b, (v1[i]-(r[i]*i1[i]))/i1[i])
    finals.append((v1[i]-(r[i]*i1[i]))/i1[i])
    err1.append(c)

avg = sum(finals)/len(finals)
print(avg)

i2 = i2/1000
ierr2 = ierr2/1000
err2 = []
finals2 = []
print("Index | v2     | v2_err  | i2     | i2_err  | v_r    | v_r_err | final  | final_err | % error")
print("-------------------------------------------------------------------------------------------------------------")

for i in range(len(r)):
    v_r = v2[i] / r[i]
    v_r_err = tl.error_mult(r[i], v2[i], rerr[i], verr2[i], v_r)
    b = i2[i] - v_r
    b_err = tl.error_add(ierr2[i], v_r_err)
    final = v2[i] / b
    finals2.append(final)
    final_err = tl.error_mult(b, v2[i], b_err, verr2[i], final)
    err2.append((final, final_err))
    
    # Calculate percent errors
    v2_percent_err = (verr2[i] / v2[i]) * 100
    i2_percent_err = (ierr2[i] / i2[i]) * 100
    v_r_percent_err = (v_r_err / v_r) * 100
    final_percent_err = (final_err / final) * 100
    
    # Display the values and percent errors
    print(f"{i:5} | {v2[i]:6.3f} | {verr2[i]:7.5f} | {i2[i]:6.3f} | {ierr2[i]:7.5f} | {v_r:6.3f} | {v_r_err:7.5f} | {final:6.3f} | {final_err:7.5f} | {final_percent_err:7.3f}%")

print(err2)

sum2 = sum(finals2)
avg2 = sum2 / len(finals2)
print(avg2)
r2 = (1/avg2 - 1/m_fit2)**-1
print(r2)
init_guess = (-0.5, 0) # guess for the best fit parameters
font_size = 12
xlabel = "Voltage (V)"
ylabel = "Current (A)"

# Now we make the plot, displayed on screen and saved in the directory, and print the best fit values
bb.plot_fit(linear, i1, v1, ierr1, verr1, init_guess=init_guess, font_size=font_size,
            xlabel=xlabel, ylabel=ylabel)
bb.plot_fit(linear, i2, v2, ierr2, verr2, init_guess=init_guess, font_size=font_size,
            xlabel=xlabel, ylabel=ylabel)


m_fit1, b_fit1 = -0.05410673394399822, 6.5022301915876435   
m_fit2, b_fit2 = -1.835005967853445, 6.502628691816137


v1_pred = linear(i1, m_fit1, b_fit1)
v2_pred = linear(i2, m_fit2, b_fit2)


rmse_value1 = rmse(v1, v1_pred)
rmse_value2 = rmse(v2, v2_pred)


print(f"RMSE for first dataset: {rmse_value1}")
print(f"RMSE for second dataset: {rmse_value2}")



