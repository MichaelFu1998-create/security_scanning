def Trebble_Bishnoi(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Trebble and Bishnoi (1987) [1]_. Returns `a_alpha`, 
        `da_alpha_dT`, and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives`  
        for more documentation. One coefficient needed.
        
        .. math::
            \alpha = e^{c_{1} \left(- \frac{T}{Tc} + 1\right)}

        References
        ----------
        .. [1] Trebble, M. A., and P. R. Bishnoi. "Development of a New Four-
           Parameter Cubic Equation of State." Fluid Phase Equilibria 35, no. 1
           (September 1, 1987): 1-18. doi:10.1016/0378-3812(87)80001-8.
        '''
        c1 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*exp(c1*(-T/Tc + 1))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = a*-c1*exp(c1*(-T/Tc + 1))/Tc
            d2a_alpha_dT2 = a*c1**2*exp(-c1*(T/Tc - 1))/Tc**2
            return a_alpha, da_alpha_dT, d2a_alpha_dT2