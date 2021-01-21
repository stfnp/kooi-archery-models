import numpy as np
from scipy.integrate import ode
from scipy.optimize import root
from math import sin, cos

# Simplified implementation (no recurve) of the static bow model found in
# B.W. Kooi and J.A. Sparenberg: On the static deformation of the bow
# Journal of Engineering Mathematics, Vol. 14, No. 1, pages 27-45, 1980.

class BowModel:    
    def __init__(self, theta_0, W, L, OH):
        self.theta_0 = theta_0                   # Function (arc length) -> limb angle
        self.W = W                               # Function (arc length) -> bending stiffness
        self.L = L                               # Length of a single limb
        self.l = self.solve_string_length(OH)    # Length of half the string

    # Returns (s, phi, x, y, K, alpha) such that the bow is in equilibrium at draw length b
    def solve_equilibrium(self, b):
        # Corresponds to functions f1 (20) and f2 (21) in the paper
        def equilibrium_condition(z):
            (K, alpha) = z
            (s, x, y, phi, i_w) = self.integrate_bending_line(b, K, alpha)
            return [
                (x[i_w] - b)*cos(alpha) + y[i_w]*sin(alpha),      # Equation (20)
                y[i_w] - (self.l - self.L + s[i_w])*cos(alpha)    # Equation (21)
            ]

        (K, alpha) = root(equilibrium_condition, [0, 0]).x                # TODO: Find initial vaues as described in the paper
        (s, x, y, phi, i_w) = self.integrate_bending_line(b, K, alpha)    # TODO: Duplicate computation
        
        return (s, x, y, phi, i_w, K, alpha)    # TODO: Create result class

    # Returns the length l of half the string such that the bow is in equilibrium at brace height OH
    def solve_string_length(self, OH):
        def equilibrium_condition(K):
            print(K)
            (s, x, y, phi, i_w) = self.integrate_bending_line(OH, K, 0)
            return x[i_w] - OH    # Equation (20) for alpha = 0 and b = OH
            
        K = root(equilibrium_condition, 0).x
        (s, x, y, phi, i_w) = self.integrate_bending_line(OH, K, 0)    # TODO: Duplicate computation
        return y[i_w] + self.L - s[i_w]    # Equation (21) for alpha = 0

    # Returns (s, phi, x, y, sw) such that the limb is in equilibrium with string force K and angle alpha
    def integrate_bending_line(self, b, K, alpha):
        s_w = self.L    # Contact point on the limb, to be determined if < L
        i_w = -1
        
        # Function that evaluates the derivatives phi'(s), x'(s), y'(s).
        # Corresponds to equations (6), (12) and (14) in the paper.
        def function(s, z):
            (phi, x, y) = z
            
            # Determine bending moment
            if s <= s_w:
                M = K/self.W(s)*((b - x)*cos(alpha) - y*sin(alpha))    # Equation (12)
            else:
                M = 0                                                  # Equation (6)
                
            return [
                M,
                sin(phi + self.theta_0(s)),   # Equation (14)
                cos(phi + self.theta_0(s))    # Equation (14)
            ]

        n_steps = 50    # TODO: Make this configurable
        
        s   = [0]
        phi = [0]
        x   = [0]
        y   = [0]
        
        sign_prev = 0
        sign_next = np.sign(phi[0] + alpha + self.theta_0([0]))    # Equation (19), look for sign change from + to -
        
        solver = ode(function)
        solver.set_integrator('dopri5')
        solver.set_initial_value([phi[0], x[0], y[0]], s[0])
        
        for i in range(0, n_steps):
            s_i = (i + 1)*self.L/n_steps                            # Calculate arc lengths
            (phi_i, x_i, y_i) = solver.integrate(s_i, step=True)    # Integrate with fixed step size

            sign_prev = sign_next
            sign_next = np.sign(phi_i + alpha + self.theta_0(s_i))    # Equation (19)
            
            #print(phi_i + alpha + self.theta_0(s_i))
            
            # If sign change from + to - and sw hasn't been assigned something else than L yet, set s_w to s_i
            if s_w == self.L and sign_next == -1 and sign_prev == +1:
                s_w = s_i
                i_w = i + 1
            
            s.append(s_i)
            phi.append(phi_i)
            x.append(x_i)
            y.append(y_i)

        return (s, x, y, phi, i_w)