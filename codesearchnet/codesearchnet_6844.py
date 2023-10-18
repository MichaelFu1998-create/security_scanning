def Gf(counts):
        r'''Estimates the ideal-gas Gibbs energy of formation at 298.15 K of an  
        organic compound using the Joback method as a function of chemical 
        structure only. 
        
        .. math::
            G_{formation} = 53.88 + \sum {G_{f,i}}
            
        In the above equation, Gibbs energy of formation is calculated in 
        kJ/mol; it is converted to J/mol here.
        
        328 compounds were used by Joback in this determination, with an 
        absolute average error of 2.0 kcal/mol, standard devaition 4.37
        kcal/mol, and AARE of 15.7%.

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Gf : float
            Estimated ideal-gas Gibbs energy of formation at 298.15 K, [J/mol]
            
        Examples
        --------
        >>> Joback.Gf({1: 2, 24: 1})
        -154540.00000000003
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Gform*count
        Gf = 53.88 + tot
        return Gf*1000