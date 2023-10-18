def Schwartzentruber(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Schwartzentruber et al. (1990) [1]_. Returns `a_alpha`, 
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`  
        for more documentation. Three coefficients needed.
        
        .. math::
            \alpha = \left(c_{4} \left(- \sqrt{\frac{T}{Tc}} + 1\right) 
            - \left(- \sqrt{\frac{T}{Tc}} + 1\right) \left(\frac{T^{2} c_{3}}
            {Tc^{2}} + \frac{T c_{2}}{Tc} + c_{1}\right) + 1\right)^{2}

        References
        ----------
        .. [1] J. Schwartzentruber, H. Renon, and S. Watanasiri, "K-values for 
           Non-Ideal Systems:An Easier Way," Chem. Eng., March 1990, 118-124.
        '''
        c1, c2, c3 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*((c4*(-sqrt(T/Tc) + 1) - (-sqrt(T/Tc) + 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1) + 1)**2)
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*((c4*(-sqrt(T/Tc) + 1) - (-sqrt(T/Tc) + 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1) + 1)*(-2*(-sqrt(T/Tc) + 1)*(2*T*c3/Tc**2 + c2/Tc) - c4*sqrt(T/Tc)/T + sqrt(T/Tc)*(T**2*c3/Tc**2 + T*c2/Tc + c1)/T))
            d2a_alpha_dT2 = a*(((-c4*(sqrt(T/Tc) - 1) + (sqrt(T/Tc) - 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1) + 1)*(8*c3*(sqrt(T/Tc) - 1)/Tc**2 + 4*sqrt(T/Tc)*(2*T*c3/Tc + c2)/(T*Tc) + c4*sqrt(T/Tc)/T**2 - sqrt(T/Tc)*(T**2*c3/Tc**2 + T*c2/Tc + c1)/T**2) + (2*(sqrt(T/Tc) - 1)*(2*T*c3/Tc + c2)/Tc - c4*sqrt(T/Tc)/T + sqrt(T/Tc)*(T**2*c3/Tc**2 + T*c2/Tc + c1)/T)**2)/2)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2