def Soave_1984(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Soave (1984) [1]_. Returns `a_alpha`, `da_alpha_dT`, and 
        `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Two coefficients needed.
        
        .. math::
            \alpha = c_{1} \left(- \frac{T}{Tc} + 1\right) + c_{2} \left(-1
            + \frac{Tc}{T}\right) + 1

        References
        ----------
        .. [1] Soave, G. "Improvement of the Van Der Waals Equation of State." 
           Chemical Engineering Science 39, no. 2 (January 1, 1984): 357-69. 
           doi:10.1016/0009-2509(84)80034-2.
        '''
        c1, c2 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*(c1*(-T/Tc + 1) + c2*(-1 + Tc/T) + 1)
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*(-c1/Tc - Tc*c2/T**2)
            d2a_alpha_dT2 = a*(2*Tc*c2/T**3)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2