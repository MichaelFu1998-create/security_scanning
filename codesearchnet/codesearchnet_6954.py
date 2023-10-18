def calculate(self, T, method):
        r'''Method to calculate low-pressure gas viscosity at
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
        mu : float
            Viscosity of the gas at T and a low pressure, [Pa*S]
        '''
        if method == GHARAGHEIZI:
            mu = Gharagheizi_gas_viscosity(T, self.Tc, self.Pc, self.MW)
        elif method == COOLPROP:
            mu = CoolProp_T_dependent_property(T, self.CASRN, 'V', 'g')
        elif method == DIPPR_PERRY_8E:
            mu = EQ102(T, *self.Perrys2_312_coeffs)
        elif method == VDI_PPDS:
            mu =  horner(self.VDI_PPDS_coeffs, T)
        elif method == YOON_THODOS:
            mu = Yoon_Thodos(T, self.Tc, self.Pc, self.MW)
        elif method == STIEL_THODOS:
            mu = Stiel_Thodos(T, self.Tc, self.Pc, self.MW)
        elif method == LUCAS_GAS:
            mu = lucas_gas(T, self.Tc, self.Pc, self.Zc, self.MW, self.dipole, CASRN=self.CASRN)
        elif method in self.tabular_data:
            mu = self.interpolate(T, method)
        return mu