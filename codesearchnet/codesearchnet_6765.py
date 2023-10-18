def Androulakis(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Androulakis et al. (1989) [1]_. Returns `a_alpha`, 
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`  
        for more documentation. Three coefficients needed.
        
        .. math::
            \alpha = c_{1} \left(- \left(\frac{T}{Tc}\right)^{\frac{2}{3}}
            + 1\right) + c_{2} \left(- \left(\frac{T}{Tc}\right)^{\frac{2}{3}} 
            + 1\right)^{2} + c_{3} \left(- \left(\frac{T}{Tc}\right)^{
            \frac{2}{3}} + 1\right)^{3} + 1

        References
        ----------
        .. [1] Androulakis, I. P., N. S. Kalospiros, and D. P. Tassios. 
           "Thermophysical Properties of Pure Polar and Nonpolar Compounds with
           a Modified VdW-711 Equation of State." Fluid Phase Equilibria 45, 
           no. 2 (April 1, 1989): 135-63. doi:10.1016/0378-3812(89)80254-7. 
        '''
        c1, c2, c3 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*(c1*(-(T/Tc)**(2/3) + 1) + c2*(-(T/Tc)**(2/3) + 1)**2 + c3*(-(T/Tc)**(2/3) + 1)**3 + 1)
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*(-2*c1*(T/Tc)**(2/3)/(3*T) - 4*c2*(T/Tc)**(2/3)*(-(T/Tc)**(2/3) + 1)/(3*T) - 2*c3*(T/Tc)**(2/3)*(-(T/Tc)**(2/3) + 1)**2/T)
            d2a_alpha_dT2 = a*(2*(T/Tc)**(2/3)*(c1 + 4*c2*(T/Tc)**(2/3) - 2*c2*((T/Tc)**(2/3) - 1) - 12*c3*(T/Tc)**(2/3)*((T/Tc)**(2/3) - 1) + 3*c3*((T/Tc)**(2/3) - 1)**2)/(9*T**2))
            return a_alpha, da_alpha_dT, d2a_alpha_dT2