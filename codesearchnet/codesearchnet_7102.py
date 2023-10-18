def calculate(self, T, method):
        r'''Method to calculate low-pressure gas thermal conductivity at
        tempearture `T` with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature of the gas, [K]
        method : str
            Name of the method to use

        Returns
        -------
        kg : float
            Thermal conductivity of the gas at T and a low pressure, [W/m/K]
        '''
        if method == GHARAGHEIZI_G:
            kg = Gharagheizi_gas(T, self.MW, self.Tb, self.Pc, self.omega)
        elif method == DIPPR_9B:
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            mug = self.mug(T) if hasattr(self.mug, '__call__') else self.mug
            kg = DIPPR9B(T, self.MW, Cvgm, mug, self.Tc)
        elif method == CHUNG:
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            mug = self.mug(T) if hasattr(self.mug, '__call__') else self.mug
            kg = Chung(T, self.MW, self.Tc, self.omega, Cvgm, mug)
        elif method == ELI_HANLEY:
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            kg = eli_hanley(T, self.MW, self.Tc, self.Vc, self.Zc, self.omega, Cvgm)
        elif method == EUCKEN_MOD:
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            mug = self.mug(T) if hasattr(self.mug, '__call__') else self.mug
            kg = Eucken_modified(self.MW, Cvgm, mug)
        elif method == EUCKEN:
            Cvgm = self.Cvgm(T) if hasattr(self.Cvgm, '__call__') else self.Cvgm
            mug = self.mug(T) if hasattr(self.mug, '__call__') else self.mug
            kg = Eucken(self.MW, Cvgm, mug)
        elif method == DIPPR_PERRY_8E:
            kg = EQ102(T, *self.Perrys2_314_coeffs)
        elif method == VDI_PPDS:
            kg = horner(self.VDI_PPDS_coeffs, T)
        elif method == BAHADORI_G:
            kg = Bahadori_gas(T, self.MW)
        elif method == COOLPROP:
            kg = CoolProp_T_dependent_property(T, self.CASRN, 'L', 'g')
        elif method in self.tabular_data:
            kg = self.interpolate(T, method)
        return kg