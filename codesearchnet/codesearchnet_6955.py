def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent gas viscosity
        at temperature `T` and pressure `P` with a given method.

        This method has no exception handling; see `TP_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate gas viscosity, [K]
        P : float
            Pressure at which to calculate gas viscosity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        mu : float
            Viscosity of the gas at T and P, [Pa*]
        '''
        if method == COOLPROP:
            mu = PropsSI('V', 'T', T, 'P', P, self.CASRN)
        elif method in self.tabular_data:
            mu = self.interpolate_P(T, P, method)
        return mu