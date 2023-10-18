def Hfus(counts):
        r'''Estimates the enthalpy of fusion of an organic compound at its 
        melting point using the Joback method as a function of chemical 
        structure only. 
        
        .. math::
            \Delta H_{fus} = -0.88 + \sum_i H_{fus,i}
            
        In the above equation, enthalpy of fusion is calculated in 
        kJ/mol; it is converted to J/mol here.
        
        For 155 compounds tested by Joback, the absolute average error was
        485.2 cal/mol  and standard deviation was 661.4 cal/mol; the average 
        relative error was 38.7%. 

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Hfus : float
            Estimated enthalpy of fusion of the compound at its melting point,
            [J/mol]
            
        Examples
        --------
        >>> Joback.Hfus({1: 2, 24: 1})
        5125.0
        '''
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Hfus*count
        Hfus = -0.88 + tot
        return Hfus*1000