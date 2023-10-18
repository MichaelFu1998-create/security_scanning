def Tb(counts):
        r'''Estimates the normal boiling temperature of an organic compound 
        using the Joback method as a function of chemical structure only.
        
        .. math::
            T_b = 198.2 + \sum_i {T_{b,i}}
            
        For 438 compounds tested by Joback, the absolute average error was
        12.91 K  and standard deviation was 17.85 K; the average relative error
        was 3.6%. 
            
        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Tb : float
            Estimated normal boiling temperature, [K]
            
        Examples
        --------
        >>> Joback.Tb({1: 2, 24: 1})
        322.11
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Tb*count
        Tb = 198.2 + tot
        return Tb