def Heyen(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives according to Heyen (1980) [1]_. Returns `a_alpha`, `da_alpha_dT`,  
        and `d2a_alpha_dT2`. See `GCEOS.a_alpha_and_derivatives` for more 
        documentation. Two coefficients needed.
        
        .. math::
            \alpha = e^{c_{1} \left(- \left(\frac{T}{Tc}\right)^{c_{2}}
            + 1\right)}

        References
        ----------
        .. [1] Heyen, G. Liquid and Vapor Properties from a Cubic Equation of 
           State. In "Proceedings of the 2nd International Conference on Phase 
           Equilibria and Fluid Properties in the Chemical Industry". DECHEMA: 
           Frankfurt, 1980; p 9-13.
        '''
        c1, c2 = self.alpha_function_coeffs
        T, Tc, a = self.T, self.Tc, self.a
        a_alpha = a*exp(c1*(1 -(T/Tc)**c2))
        if not full:
            return a_alpha
        else:
            da_alpha_dT = -a*c1*c2*(T/Tc)**c2*exp(c1*(-(T/Tc)**c2 + 1))/T
            d2a_alpha_dT2 = a*c1*c2*(T/Tc)**c2*(c1*c2*(T/Tc)**c2 - c2 + 1)*exp(-c1*((T/Tc)**c2 - 1))/T**2
            return a_alpha, da_alpha_dT, d2a_alpha_dT2