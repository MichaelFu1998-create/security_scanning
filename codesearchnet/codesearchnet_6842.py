def Vc(counts):
        r'''Estimates the critcal volume of an organic compound using the 
        Joback method as a function of chemical structure only. 
        
        .. math::
            V_c = 17.5 + \sum_i {V_{c,i}}
            
        In the above equation, critical volume is calculated in cm^3/mol; it 
        is converted to m^3/mol here.
        
        310 compounds were used by Joback in this determination, with an 
        absolute average error of 7.54 cm^3/mol, standard devaition 13.16
        cm^3/mol, and AARE of 2.27%.

        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]

        Returns
        -------
        Vc : float
            Estimated critical volume, [m^3/mol]
            
        Examples
        --------
        >>> Joback.Vc({1: 2, 24: 1})
        0.0002095
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Vc*count
        Vc = 17.5 + tot
        return Vc*1E-6