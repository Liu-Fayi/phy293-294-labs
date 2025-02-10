import math
import tools as tl
import fit_black_box as bb
import numpy as np

# Constants and measured values
mue_0 = 4 * math.pi * 10**-7         
R = 0.326/2                          
R_err = 0.005/2                      
n = 130

# Field offset values from extra_field analysis
b_e, b_e_unc = 7.279481489311506e-5, 1.313424340798893e-5 
k = 1/math.sqrt(2) * (4/5)**(3/2) * mue_0 * n / R
k_err = k * (R_err/R)

# Calculate I_o = b_e/k with standard propagation for a quotient:

I_o = b_e/k
I_o_err = I_o * np.sqrt((b_e_unc/b_e)**2 + (k_err/k)**2)

print(f"k = {k:.2e} +/- {k_err:.2e}")
print(f"I_o relative error: {I_o_err/I_o:.2e}")

print("I_o: ", I_o, "+/-", I_o_err)

# ---------------------------
# Fixed-current fit propagation:
i = 1.076                
a, a_err = 0.004006761994742138,  4.674028233227996e-5

# Define X = (a*k) * ( i + 1/sqrt2 * I_o )
term1 = a * k
term1_rel = np.sqrt((a_err/a)**2 + (k_err/k)**2)
term2 = i + (1/math.sqrt(2))*I_o
# Assume i is exact so its uncertainty comes solely from I_o:
term2_err = (1/math.sqrt(2)) * I_o_err
term2_rel = term2_err/term2

X = term1 * term2
X_rel = np.sqrt(term1_rel**2 + term2_rel**2)

e_ratio_I = 1/(X**2)
e_ratio_I_err = 2 * e_ratio_I * X_rel

print(f"Fixed current fit: e/m = {e_ratio_I:.2e} +/- {e_ratio_I_err:.2e}")

# ---------------------------
# Fixed-voltage fit propagation:
v = 186.01                            
a_fit, a_fit_unc = 0.0640095857828037, 0.0016815877487173848

# For fixed-voltage method assume:
# e_ratio_V = 1/(a_fit * k)^2.
X_v = a_fit/(math.sqrt(v)) * k

X_v_rel = np.sqrt((a_fit_unc/a_fit)**2 + (k_err/k)**2 + (0.01/v)**2)

e_ratio_V = 1/(X_v**2)
e_ratio_V_err = 2 * e_ratio_V * X_v_rel

print(f"Fixed voltage fit: e/m = {e_ratio_V:.2e} +/- {e_ratio_V_err:.2e}")

#compare to the accepted value
accepted = 1.758820024*10**11

#percent error
percent_error_I = abs(e_ratio_I - accepted)/accepted
percent_error_V = abs(e_ratio_V - accepted)/accepted
#in percent
percent_error_I *= 100
percent_error_V *= 100

print(f"Percent error for fixed current fit: {percent_error_I:.3f}%")
print(f"Percent error for fixed voltage fit: {percent_error_V:.3f}%")


avg_ratio = (e_ratio_I + e_ratio_V)/2
avg_ratio_err = np.sqrt(e_ratio_I_err**2 + e_ratio_V_err**2)/2

print(f"Average e/m ratio: {avg_ratio:.4e} +/- {avg_ratio_err:.4e}")
print(f"Percent error for average: {abs(avg_ratio - accepted)/accepted*100:.3f}%")


print("Percent uncertainty for fixed current fit: ", format(e_ratio_I_err/e_ratio_I*100,".2f"))
print("Percent uncertainty for fixed voltage fit: ", format(e_ratio_V_err/e_ratio_V*100,".2f"))
print("Percent uncertainty for average: ", format(avg_ratio_err/avg_ratio*100,".2f"))



print(f"Fixed current fit: e/m = {e_ratio_I:.2e} +/- {e_ratio_I_err:.2e} eV/T")
print(f"Fixed voltage fit: e/m = {e_ratio_V:.2e} +/- {e_ratio_V_err:.2e} eV/T")



# vizualize the data and unc in comparison to the accepted value
import matplotlib.pyplot as plt

plt.errorbar([1,2,3],[e_ratio_I, e_ratio_V,avg_ratio], yerr=[e_ratio_I_err, e_ratio_V_err,avg_ratio_err], fmt='o', label="Calculated values")
plt.axhline(y=accepted, color='r', linestyle='-', label="Accepted value")
plt.xlabel("Method")
plt.xticks([1,2,3],["Fixed current", "Fixed voltage", "Average"])
plt.ylabel("e/m ratio")
plt.title("e/m ratio calculated using two methods")
plt.legend()



plt.show()



