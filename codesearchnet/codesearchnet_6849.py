def Cpig(self, T):
        r'''Computes ideal-gas heat capacity at a specified temperature 
        of an organic compound using the Joback method as a function of  
        chemical structure only. 
        
        .. math::
            C_p^{ig} = \sum_i a_i - 37.93 + \left[ \sum_i b_i + 0.210 \right] T
            + \left[ \sum_i c_i - 3.91 \cdot 10^{-4} \right] T^2 
            + \left[\sum_i d_i + 2.06 \cdot 10^{-7}\right] T^3
        
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        Cpig : float
            Ideal-gas heat capacity, [J/mol/K]
            
        Examples
        --------
        >>> J = Joback('CC(=O)C')
        >>> J.Cpig(300)
        75.32642000000001
        '''
        if self.calculated_Cpig_coeffs is None:
            self.calculated_Cpig_coeffs = Joback.Cpig_coeffs(self.counts)
        return horner(reversed(self.calculated_Cpig_coeffs), T)