def Coquelet(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Coquelet et al. (2004) [1]_. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Three coefficients needed.
        
        .. math::
            \alpha = e^{c_{1} \left(- \frac{T}{Tc} + 1\right) \left(c_{2} 
            \left(- \sqrt{\frac{T}{Tc}} + 1\right)^{2} + c_{3} 
            \left(- \sqrt{\frac{T}{Tc}} + 1\right)^{3} + 1\right)^{2}}

        References
        ----------
        .. [1] Coquelet, C., A. Chapoy, and D. Richon. "Development of a New 
           Alpha Function for the Peng–Robinson Equation of State: Comparative 
           Study of Alpha Function Models for Pure Gases (Natural Gas 
           Components) and Water-Gas Systems." International Journal of 
           Thermophysics 25, no. 1 (January 1, 2004): 133-58. 
           doi:10.1023/B:IJOT.0000022331.46865.2f.
        '''
        c1, c2, c3 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*(exp(c1*(-T/Tc + 1)*(c2*(-sqrt(T/Tc) + 1)**2 + c3*(-sqrt(T/Tc) + 1)**3 + 1)**2))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*((c1*(-T/Tc + 1)*(-2*c2*sqrt(T/Tc)*(-sqrt(T/Tc) + 1)/T - 3*c3*sqrt(T/Tc)*(-sqrt(T/Tc) + 1)**2/T)*(c2*(-sqrt(T/Tc) + 1)**2 + c3*(-sqrt(T/Tc) + 1)**3 + 1) - c1*(c2*(-sqrt(T/Tc) + 1)**2 + c3*(-sqrt(T/Tc) + 1)**3 + 1)**2/Tc)*exp(c1*(-T/Tc + 1)*(c2*(-sqrt(T/Tc) + 1)**2 + c3*(-sqrt(T/Tc) + 1)**3 + 1)**2))
            d2a_alpha_dT2 = a*(c1*(c1*(-(c2*(sqrt(T/Tc) - 1)**2 - c3*(sqrt(T/Tc) - 1)**3 + 1)/Tc + sqrt(T/Tc)*(-2*c2 + 3*c3*(sqrt(T/Tc) - 1))*(sqrt(T/Tc) - 1)*(T/Tc - 1)/T)**2*(c2*(sqrt(T/Tc) - 1)**2 - c3*(sqrt(T/Tc) - 1)**3 + 1)**2 - ((T/Tc - 1)*(c2*(sqrt(T/Tc) - 1)**2 - c3*(sqrt(T/Tc) - 1)**3 + 1)*(2*c2/Tc - 6*c3*(sqrt(T/Tc) - 1)/Tc - 2*c2*sqrt(T/Tc)*(sqrt(T/Tc) - 1)/T + 3*c3*sqrt(T/Tc)*(sqrt(T/Tc) - 1)**2/T) + 4*sqrt(T/Tc)*(2*c2 - 3*c3*(sqrt(T/Tc) - 1))*(sqrt(T/Tc) - 1)*(c2*(sqrt(T/Tc) - 1)**2 - c3*(sqrt(T/Tc) - 1)**3 + 1)/Tc + (2*c2 - 3*c3*(sqrt(T/Tc) - 1))**2*(sqrt(T/Tc) - 1)**2*(T/Tc - 1)/Tc)/(2*T))*exp(-c1*(T/Tc - 1)*(c2*(sqrt(T/Tc) - 1)**2 - c3*(sqrt(T/Tc) - 1)**3 + 1)**2))
            return a_alpha, da_alpha_dT, d2a_alpha_dT2