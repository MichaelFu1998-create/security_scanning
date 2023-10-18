def Pc(counts, atom_count):
        r'''Estimates the critcal pressure of an organic compound using the 
        Joback method as a function of chemical structure only. This 
        correlation was developed using the actual number of atoms forming 
        the molecule as well.
        
        .. math::
            P_c = \left [0.113 + 0.0032N_A - \sum_i {P_{c,i}}\right ]^{-2}
            
        In the above equation, critical pressure is calculated in bar; it is
        converted to Pa here.
        
        392 compounds were used by Joback in this determination, with an 
        absolute average error of 2.06 bar, standard devaition 3.2 bar, and
        AARE of 5.2%.
        
        Parameters
        ----------
        counts : dict
            Dictionary of Joback groups present (numerically indexed) and their
            counts, [-]
        atom_count : int
            Total number of atoms (including hydrogens) in the molecule, [-]

        Returns
        -------
        Pc : float
            Estimated critical pressure, [Pa]
            
        Examples
        --------
        >>> Joback.Pc({1: 2, 24: 1}, 10)
        4802499.604994407
        '''        
        tot = 0.0
        for group, count in counts.items():
            tot += joback_groups_id_dict[group].Pc*count
        Pc = (0.113 + 0.0032*atom_count - tot)**-2
        return Pc*1E5