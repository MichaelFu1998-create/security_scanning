def Tm(counts):
        r'''Estimates the melting temperature of an organic compound using the 
        Joback method as a function of chemical structure only.
        
        .. math::
            T_m = 122.5 + \sum_i {T_{m,i}}
            
        For 388 compounds tested by Joback, the absolute average error was
        22.6 K  and standard deviation was 24.68 K; the average relative error
        was 11.2%. 

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Tm : float
            Estimated melting temperature, [K]
            
        Examples
        --------
        >>> Joback.Tm({1: 2, 24: 1})
        173.5
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Tm*count
        Tm = 122.5 + tot
        return Tm