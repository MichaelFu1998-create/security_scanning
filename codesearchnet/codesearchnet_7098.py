def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent liquid thermal conductivity
        at temperature `T` and pressure `P` with a given method.

        This method has no exception handling; see `TP_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate liquid thermal conductivity, [K]
        P : float
            Pressure at which to calculate liquid thermal conductivity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        kl : float
            Thermal conductivity of the liquid at T and P, [W/m/K]
        '''
        if method == DIPPR_9G:
            kl = self.T_dependent_property(T)
            kl = DIPPR9G(T, P, self.Tc, self.Pc, kl)
        elif method == MISSENARD:
            kl = self.T_dependent_property(T)
            kl = Missenard(T, P, self.Tc, self.Pc, kl)
        elif method == COOLPROP:
            kl = PropsSI('L', 'T', T, 'P', P, self.CASRN)
        elif method in self.tabular_data:
            kl = self.interpolate_P(T, P, method)
        return kl