def calculate_integral_over_T(self, T1, T2):
        r'''Method to compute the entropy integral of heat capacity from 
         `T1` to `T2`.
            
        Parameters
        ----------
        T1 : float
            Initial temperature, [K]
        T2 : float
            Final temperature, [K]
            
        Returns
        -------
        dS : float
            Entropy difference between `T1` and `T2`, [J/mol/K]
        '''        
        return (Zabransky_quasi_polynomial_integral_over_T(T2, self.Tc, *self.coeffs)
               - Zabransky_quasi_polynomial_integral_over_T(T1, self.Tc, *self.coeffs))