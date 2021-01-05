from bow_model import BowModel
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Define bow parameters
L = 0.8
l = 0.75
theta0 = UnivariateSpline(np.linspace(0, L, 5), np.linspace(0, 0, 5))
W = UnivariateSpline(np.linspace(0, L, 5), np.linspace(10, 5, 5))

# Create an instance of the bow model
model = BowModel(theta0, W, L, l)

# Solve for equilibrium at different draw lengths and plot the results
for b in np.linspace(0.25, 0.7, 5):
    [s, phi, x, y] = model.solve_equilibrium(b)
    plt.plot(x, y, 'b')
    plt.plot([b, x[-1]], [0, y[-1]], 'r')

plt.title('Bow shapes')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()