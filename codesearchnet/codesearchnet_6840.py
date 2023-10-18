def Tc(counts, Tb=None):
        r'''Estimates the critcal temperature of an organic compound using the 
        Joback method as a function of chemical structure only, or optionally
        improved by using an experimental boiling point. If the experimental
        boiling point is not provided it will be estimated with the Joback
        method as well.
        
        .. math::
            T_c = T_b \left[0.584 + 0.965 \sum_i {T_{c,i}}
            - \left(\sum_i {T_{c,i}}\right)^2 \right]^{-1}
            
        For 409 compounds tested by Joback, the absolute average error was
        4.76 K  and standard deviation was 6.94 K; the average relative error
        was 0.81%. 
        
        Appendix BI of Joback's work lists 409 estimated critical temperatures.
        
        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]
        Tb : float, optional
            Experimental normal boiling temperature, [K]

        Returns
        -------
        Tc : float
            Estimated critical temperature, [K]
            
        Examples
        --------
        >>> Joback.Tc({1: 2, 24: 1}, Tb=322.11)
        500.5590049525365
        '''        
        if Tb is None:
            Tb = Joback.Tb(counts)
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Tc*count
        Tc = Tb/(0.584 + 0.965*tot - tot*tot)
        return Tc