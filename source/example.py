from bow_model import BowModel
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Define bow parameters
L = 0.8
l = 0.75
theta_0 = UnivariateSpline(np.linspace(0, L, 5), np.array([0, -0.05, -0.1, -0.4, -1.2]))
W = UnivariateSpline(np.linspace(0, L, 5), np.linspace(10, 8, 5))

# Create an instance of the bow model
model = BowModel(theta_0, W, L, l)

# Solve for equilibrium at different draw lengths and plot the results
for b in np.linspace(0.25, 0.7, 5):
    (s, x, y, phi, i_w, K, alpha) = model.solve_equilibrium(b)
    plt.plot(x, y, 'b')
    plt.plot([b, x[i_w]], [0, y[i_w]], 'r')

#b = 0.4
#(s, x, y, phi, i_w, K, alpha) = model.solve_equilibrium(b)
#plt.plot(x, y, 'b')
#plt.plot([b, x[i_w]], [0, y[i_w]], 'r')

plt.title('Bow shapes')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()