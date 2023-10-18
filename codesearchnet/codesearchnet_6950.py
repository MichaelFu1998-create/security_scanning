def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent liquid viscosity at
        temperature `T` and pressure `P` with a given method.

        This method has no exception handling; see `TP_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate viscosity, [K]
        P : float
            Pressure at which to calculate viscosity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        mu : float
            Viscosity of the liquid at T and P, [Pa*S]
        '''
        if method == LUCAS:
            mu = self.T_dependent_property(T)
            Psat = self.Psat(T) if hasattr(self.Psat, '__call__') else self.Psat
            mu = Lucas(T, P, self.Tc, self.Pc, self.omega, Psat, mu)
        elif method == COOLPROP:
            mu = PropsSI('V', 'T', T, 'P', P, self.CASRN)
        elif method in self.tabular_data:
            mu = self.interpolate_P(T, P, method)
        return mu