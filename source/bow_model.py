import numpy as np
from scipy.integrate import ode
from scipy.optimize import root
from math import sin, cos

# Simplified implementation (no recurve) of the static bow model found in
# B.W. Kooi and J.A. Sparenberg: On the static deformation of the bow
# Journal of Engineering Mathematics, Vol. 14, No. 1, pages 27-45, 1980.
class BowModel:    
    def __init__(self, theta0, W, L, l):
        self.theta0 = theta0    # Function (arc length) -> limb angle
        self.W = W              # Function (arc length) -> bending stiffness
        self.L = L              # Length of the limb
        self.l = l              # Length of the string

    # Returns (s, phi, x, y) such that the bow is in equilibrium at draw length b
    def solve_equilibrium(self, b):
        # Corresponds to equations (20) and (21) in the paper
        def equilibrium_function(z):
            (K, alpha) = z
            [s, phi, x, y] = self.integrate_bending_line(b, K, alpha)
            return [x[-1] - b + self.l*sin(alpha),
                    y[-1] - self.l*cos(alpha)]

        res = root(equilibrium_function, [0, 0])
        return self.integrate_bending_line(b, *res.x)

    # Returns (s, phi, x, y) such that the limb is in equilibrium at the string force K and angle alpha
    def integrate_bending_line(self, b, K, alpha):
        # Corresponds to equations (12) and (14) in the paper
        def ode_function(s, z):
            (phi, x, y) = z
            return [K/self.W(s)*((b - x)*cos(alpha) - y*sin(alpha)),
                    sin(phi + self.theta0(s)),
                    cos(phi + self.theta0(s))]

        solution = ([], [], [], [])
        def output_function(s, z):
            solution[0].append(s)
            solution[1].append(z[0])
            solution[2].append(z[1])
            solution[3].append(z[2])

        solver = ode(ode_function).set_integrator('dopri5', atol=1e-9, rtol=1e-9)
        solver.set_solout(output_function)
        solver.set_initial_value([0, 0, 0], 0)
        solver.integrate(self.L)

        return solution