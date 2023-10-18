def calculate(self, T, method):
        r'''Method to calculate vapor pressure of a fluid at temperature `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at calculate vapor pressure, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Psat : float
            Vapor pressure at T, [pa]
        '''
        if method == WAGNER_MCGARRY:
            Psat = Wagner_original(T, self.WAGNER_MCGARRY_Tc, self.WAGNER_MCGARRY_Pc, *self.WAGNER_MCGARRY_coefs)
        elif method == WAGNER_POLING:
            Psat = Wagner(T, self.WAGNER_POLING_Tc, self.WAGNER_POLING_Pc, *self.WAGNER_POLING_coefs)
        elif method == ANTOINE_EXTENDED_POLING:
            Psat = TRC_Antoine_extended(T, *self.ANTOINE_EXTENDED_POLING_coefs)
        elif method == ANTOINE_POLING:
            A, B, C = self.ANTOINE_POLING_coefs
            Psat = Antoine(T, A, B, C, base=10.0)
        elif method == DIPPR_PERRY_8E:
            Psat = EQ101(T, *self.Perrys2_8_coeffs)
        elif method == VDI_PPDS:
            Psat = Wagner(T, self.VDI_PPDS_Tc, self.VDI_PPDS_Pc, *self.VDI_PPDS_coeffs)
        elif method == COOLPROP:
            Psat = PropsSI('P','T', T,'Q',0, self.CASRN)
        elif method == BOILING_CRITICAL:
            Psat = boiling_critical_relation(T, self.Tb, self.Tc, self.Pc)
        elif method == LEE_KESLER_PSAT:
            Psat = Lee_Kesler(T, self.Tc, self.Pc, self.omega)
        elif method == AMBROSE_WALTON:
            Psat = Ambrose_Walton(T, self.Tc, self.Pc, self.omega)
        elif method == SANJARI:
            Psat = Sanjari(T, self.Tc, self.Pc, self.omega)
        elif method == EDALAT:
            Psat = Edalat(T, self.Tc, self.Pc, self.omega)
        elif method == EOS:
            Psat = self.eos[0].Psat(T)
        elif method in self.tabular_data:
            Psat = self.interpolate(T, method)
        return Psat