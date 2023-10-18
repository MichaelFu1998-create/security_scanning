def calculate(self, T, method):
        r'''Method to calculate low-pressure liquid thermal conductivity at
        tempearture `T` with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature of the liquid, [K]
        method : str
            Name of the method to use

        Returns
        -------
        kl : float
            Thermal conductivity of the liquid at T and a low pressure, [W/m/K]
        '''
        if method == SHEFFY_JOHNSON:
            kl = Sheffy_Johnson(T, self.MW, self.Tm)
        elif method == SATO_RIEDEL:
            kl = Sato_Riedel(T, self.MW, self.Tb, self.Tc)
        elif method == GHARAGHEIZI_L:
            kl = Gharagheizi_liquid(T, self.MW, self.Tb, self.Pc, self.omega)
        elif method == NICOLA:
            kl = Nicola(T, self.MW, self.Tc, self.Pc, self.omega)
        elif method == NICOLA_ORIGINAL:
            kl = Nicola_original(T, self.MW, self.Tc, self.omega, self.Hfus)
        elif method == LAKSHMI_PRASAD:
            kl = Lakshmi_Prasad(T, self.MW)
        elif method == BAHADORI_L:
            kl = Bahadori_liquid(T, self.MW)
        elif method == DIPPR_PERRY_8E:
            kl = EQ100(T, *self.Perrys2_315_coeffs)
        elif method == VDI_PPDS:
            kl = horner(self.VDI_PPDS_coeffs, T)
        elif method == COOLPROP:
            kl = CoolProp_T_dependent_property(T, self.CASRN, 'L', 'l')
        elif method in self.tabular_data:
            kl = self.interpolate(T, method)
        return kl