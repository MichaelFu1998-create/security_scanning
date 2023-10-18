def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent gas thermal conductivity
        at temperature `T` and pressure `P` with a given method.

        This method has no exception handling; see `TP_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate gas thermal conductivity, [K]
        P : float
            Pressure at which to calculate gas thermal conductivity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        kg : float
            Thermal conductivity of the gas at T and P, [W/m/K]
        '''
        if method == ELI_HANLEY_DENSE:
            Vmg = self.Vmg(T, P) if hasattr(self.Vmg, '__call__') else self.Vmg
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            kg = eli_hanley_dense(T, self.MW, self.Tc, self.Vc, self.Zc, self.omega, Cvgm, Vmg)
        elif method == CHUNG_DENSE:
            Vmg = self.Vmg(T, P) if hasattr(self.Vmg, '__call__') else self.Vmg
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            mug = self.mug(T, P) if hasattr(self.mug, '__call__') else self.mug
            kg = chung_dense(T, self.MW, self.Tc, self.Vc, self.omega, Cvgm, Vmg, mug, self.dipole)
        elif method == STIEL_THODOS_DENSE:
            kg = self.T_dependent_property(T)
            Vmg = self.Vmg(T, P) if hasattr(self.Vmg, '__call__') else self.Vmg
            kg = stiel_thodos_dense(T, self.MW, self.Tc, self.Pc, self.Vc, self.Zc, Vmg, kg)
        elif method == COOLPROP:
            kg = PropsSI('L', 'T', T, 'P', P, self.CASRN)
        elif method in self.tabular_data:
            kg = self.interpolate_P(T, P, method)
        return kg