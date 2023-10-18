def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent liquid molar volume at
        temperature `T` and pressure `P` with a given method.

        This method has no exception handling; see `TP_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate molar volume, [K]
        P : float
            Pressure at which to calculate molar volume, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Vm : float
            Molar volume of the liquid at T and P, [m^3/mol]
        '''
        if method == COSTALD_COMPRESSED:
            Vm = self.T_dependent_property(T)
            Psat = self.Psat(T) if hasattr(self.Psat, '__call__') else self.Psat
            Vm = COSTALD_compressed(T, P, Psat, self.Tc, self.Pc, self.omega, Vm)
        elif method == COOLPROP:
            Vm = 1./PropsSI('DMOLAR', 'T', T, 'P', P, self.CASRN)
        elif method == EOS:
            self.eos[0] = self.eos[0].to_TP(T=T, P=P)
            Vm = self.eos[0].V_l
        elif method in self.tabular_data:
            Vm = self.interpolate_P(T, P, method)
        return Vm