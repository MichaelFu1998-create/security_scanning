def calculate_P(self, T, P, method):
        r'''Method to calculate pressure-dependent gas molar volume at
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
            Molar volume of the gas at T and P, [m^3/mol]
        '''
        if method == EOS:
            self.eos[0] = self.eos[0].to_TP(T=T, P=P)
            Vm = self.eos[0].V_g
        elif method == TSONOPOULOS_EXTENDED:
            B = BVirial_Tsonopoulos_extended(T, self.Tc, self.Pc, self.omega, dipole=self.dipole)
            Vm = ideal_gas(T, P) + B
        elif method == TSONOPOULOS:
            B = BVirial_Tsonopoulos(T, self.Tc, self.Pc, self.omega)
            Vm = ideal_gas(T, P) + B
        elif method == ABBOTT:
            B = BVirial_Abbott(T, self.Tc, self.Pc, self.omega)
            Vm = ideal_gas(T, P) + B
        elif method == PITZER_CURL:
            B = BVirial_Pitzer_Curl(T, self.Tc, self.Pc, self.omega)
            Vm = ideal_gas(T, P) + B
        elif method == CRC_VIRIAL:
            a1, a2, a3, a4, a5 = self.CRC_VIRIAL_coeffs
            t = 298.15/T - 1.
            B = (a1 + a2*t + a3*t**2 + a4*t**3 + a5*t**4)/1E6
            Vm = ideal_gas(T, P) + B
        elif method == IDEAL:
            Vm = ideal_gas(T, P)
        elif method == COOLPROP:
            Vm = 1./PropsSI('DMOLAR', 'T', T, 'P', P, self.CASRN)
        elif method in self.tabular_data:
            Vm = self.interpolate_P(T, P, method)
        return Vm