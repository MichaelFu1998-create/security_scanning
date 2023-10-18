def Cpig_coeffs(counts):
        r'''Computes the ideal-gas polynomial heat capacity coefficients 
        of an organic compound using the Joback method as a function of  
        chemical structure only. 
        
        .. math::
            C_p^{ig} = \sum_i a_i - 37.93 + \left[ \sum_i b_i + 0.210 \right] T
            + \left[ \sum_i c_i - 3.91 \cdot 10^{-4} \right] T^2 
            + \left[\sum_i d_i + 2.06 \cdot 10^{-7}\right] T^3
        
        288 compounds were used by Joback in this determination. No overall 
        error was reported.

        The ideal gas heat capacity values used in developing the heat 
        capacity polynomials used 9 data points between 298 K and 1000 K.

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        coefficients : list[float]
            Coefficients which will result in a calculated heat capacity in
            in units of J/mol/K, [-]
            
        Examples
        --------
        >>> c = Joback.Cpig_coeffs({1: 2, 24: 1})
        >>> c
        [7.520000000000003, 0.26084, -0.0001207, 1.545999999999998e-08]
        >>> Cp = lambda T : c[0] + c[1]*T + c[2]*T**2 + c[3]*T**3
        >>> Cp(300)
        75.32642000000001
        '''
        a, b, c, d = 0.0, 0.0, 0.0, 0.0
        for group, count in counts.items():
            a += joback_groups_id_dict[group].Cpa*count
            b += joback_groups_id_dict[group].Cpb*count
            c += joback_groups_id_dict[group].Cpc*count
            d += joback_groups_id_dict[group].Cpd*count
        a -= 37.93
        b += 0.210
        c -= 3.91E-4
        d += 2.06E-7
        return [a, b, c, d]