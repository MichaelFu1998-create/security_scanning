def mul_coeffs(counts):
        r'''Computes the liquid phase viscosity Joback coefficients 
        of an organic compound using the Joback method as a function of  
        chemical structure only. 
        
        .. math::
            \mu_{liq} = \text{MW} \exp\left( \frac{ \sum_i \mu_a - 597.82}{T} 
            + \sum_i \mu_b - 11.202 \right)
            
        288 compounds were used by Joback in this determination. No overall 
        error was reported.

        The liquid viscosity data used was specified to be at "several 
        temperatures for each compound" only. A small and unspecified number
        of compounds were used in this estimation.

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        coefficients : list[float]
            Coefficients which will result in a liquid viscosity in
            in units of Pa*s, [-]
            
        Examples
        --------
        >>> mu_ab = Joback.mul_coeffs({1: 2, 24: 1})
        >>> mu_ab
        [839.1099999999998, -14.99]
        >>> MW = 58.041864812
        >>> mul = lambda T : MW*exp(mu_ab[0]/T + mu_ab[1])
        >>> mul(300)
        0.0002940378347162687
        '''
        a, b = 0.0, 0.0
        for group, count in counts.items():
            a += joback_groups_id_dict[group].mua*count
            b += joback_groups_id_dict[group].mub*count
        a -= 597.82
        b -= 11.202
        return [a, b]