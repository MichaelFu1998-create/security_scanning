def calculate_integral(self, T1, T2):
        r'''Method to compute the enthalpy integral of heat capacity from 
         `T1` to `T2`.
            
        Parameters
        ----------
        T1 : float
            Initial temperature, [K]
        T2 : float
            Final temperature, [K]
            
        Returns
        -------
        dH : float
            Enthalpy difference between `T1` and `T2`, [J/mol]
        '''        
        return (Zabransky_quasi_polynomial_integral(T2, self.Tc, *self.coeffs)
               - Zabransky_quasi_polynomial_integral(T1, self.Tc, *self.coeffs))