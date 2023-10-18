def Yu_Lu(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Yu and Lu (1987) [1]_. Returns `a_alpha`, 
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`  
        for more documentation. Four coefficients needed.
        
        .. math::
            \alpha = 10^{c_{4} \left(- \frac{T}{Tc} + 1\right) \left(
            \frac{T^{2} c_{3}}{Tc^{2}} + \frac{T c_{2}}{Tc} + c_{1}\right)}

        References
        ----------
        .. [1] Yu, Jin-Min, and Benjamin C. -Y. Lu. "A Three-Parameter Cubic 
           Equation of State for Asymmetric Mixture Density Calculations." 
           Fluid Phase Equilibria 34, no. 1 (January 1, 1987): 1-19. 
           doi:10.1016/0378-3812(87)85047-1. 
        '''
        c1, c2, c3, c4 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*10**(c4*(-T/Tc + 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*(10**(c4*(-T/Tc + 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1))*(c4*(-T/Tc + 1)*(2*T*c3/Tc**2 + c2/Tc) - c4*(T**2*c3/Tc**2 + T*c2/Tc + c1)/Tc)*log(10))
            d2a_alpha_dT2 = a*(10**(-c4*(T/Tc - 1)*(T**2*c3/Tc**2 + T*c2/Tc + c1))*c4*(-4*T*c3/Tc - 2*c2 - 2*c3*(T/Tc - 1) + c4*(T**2*c3/Tc**2 + T*c2/Tc + c1 + (T/Tc - 1)*(2*T*c3/Tc + c2))**2*log(10))*log(10)/Tc**2)
            return a_alpha, da_alpha_dT, d2a_alpha_dT2