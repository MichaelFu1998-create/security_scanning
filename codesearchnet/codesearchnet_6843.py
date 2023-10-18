def Hf(counts):
        r'''Estimates the ideal-gas enthalpy of formation at 298.15 K of an  
        organic compound using the Joback method as a function of chemical 
        structure only. 
        
        .. math::
            H_{formation} = 68.29 + \sum_i {H_{f,i}}
            
        In the above equation, enthalpy of formation is calculated in kJ/mol;  
        it is converted to J/mol here.
        
        370 compounds were used by Joback in this determination, with an 
        absolute average error of 2.2 kcal/mol, standard devaition 2.0 
        kcal/mol, and AARE of 15.2%.
        
        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Hf : float
            Estimated ideal-gas enthalpy of formation at 298.15 K, [J/mol]
            
        Examples
        --------
        >>> Joback.Hf({1: 2, 24: 1})
        -217829.99999999997
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Hform*count
        Hf = 68.29 + tot
        return Hf*1000