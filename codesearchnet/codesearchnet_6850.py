def mul(self, T):
        r'''Computes liquid viscosity at a specified temperature 
        of an organic compound using the Joback method as a function of  
        chemical structure only. 
        
        .. math::
            \mu_{liq} = \text{MW} \exp\left( \frac{ \sum_i \mu_a - 597.82}{T}
            + \sum_i \mu_b - 11.202 \right)
            
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        mul : float
            Liquid viscosity, [Pa*s]
            
        Examples
        --------
        >>> J = Joback('CC(=O)C')
        >>> J.mul(300)
        0.0002940378347162687
        '''
        if self.calculated_mul_coeffs is None:
            self.calculated_mul_coeffs = Joback.mul_coeffs(self.counts)
        a, b = self.calculated_mul_coeffs
        return self.MW*exp(a/T + b)