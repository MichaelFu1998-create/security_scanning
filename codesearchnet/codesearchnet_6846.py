def Hvap(counts):
        r'''Estimates the enthalpy of vaporization of an organic compound at  
        its normal boiling point using the Joback method as a function of  
        chemical structure only. 
        
        .. math::
            \Delta H_{vap} = 15.30 + \sum_i H_{vap,i}
            
        In the above equation, enthalpy of fusion is calculated in 
        kJ/mol; it is converted to J/mol here.
        
        For 368 compounds tested by Joback, the absolute average error was
        303.5 cal/mol  and standard deviation was 429 cal/mol; the average 
        relative error was 3.88%. 
        
        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Hvap : float
            Estimated enthalpy of vaporization of the compound at its normal
            boiling point, [J/mol]
            
        Examples
        --------
        >>> Joback.Hvap({1: 2, 24: 1})
        29018.0
        '''
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Hvap*count
        Hvap = 15.3 + tot
        return Hvap*1000