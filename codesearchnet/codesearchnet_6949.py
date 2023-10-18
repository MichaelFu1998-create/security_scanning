def calculate(self, T, method):
        r'''Method to calculate low-pressure liquid viscosity at tempearture
        `T` with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate viscosity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        mu : float
            Viscosity of the liquid at T and a low pressure, [Pa*S]
        '''
        if method == DUTT_PRASAD:
            A, B, C = self.DUTT_PRASAD_coeffs
            mu = ViswanathNatarajan3(T, A, B, C, )
        elif method == VISWANATH_NATARAJAN_3:
            A, B, C = self.VISWANATH_NATARAJAN_3_coeffs
            mu = ViswanathNatarajan3(T, A, B, C)
        elif method == VISWANATH_NATARAJAN_2:
            A, B = self.VISWANATH_NATARAJAN_2_coeffs
            mu = ViswanathNatarajan2(T, self.VISWANATH_NATARAJAN_2_coeffs[0], self.VISWANATH_NATARAJAN_2_coeffs[1])
        elif method == VISWANATH_NATARAJAN_2E:
            C, D = self.VISWANATH_NATARAJAN_2E_coeffs
            mu = ViswanathNatarajan2Exponential(T, C, D)
        elif method == DIPPR_PERRY_8E:
            mu = EQ101(T, *self.Perrys2_313_coeffs)
        elif method == COOLPROP:
            mu = CoolProp_T_dependent_property(T, self.CASRN, 'V', 'l')
        elif method == LETSOU_STIEL:
            mu = Letsou_Stiel(T, self.MW, self.Tc, self.Pc, self.omega)
        elif method == PRZEDZIECKI_SRIDHAR:
            Vml = self.Vml(T) if hasattr(self.Vml, '__call__') else self.Vml
            mu = Przedziecki_Sridhar(T, self.Tm, self.Tc, self.Pc, self.Vc, Vml, self.omega, self.MW)
        elif method == VDI_PPDS:
            A, B, C, D, E = self.VDI_PPDS_coeffs
            term = (C - T)/(T-D)
            if term < 0:
                term1 = -((T - C)/(T-D))**(1/3.)
            else:
                term1 = term**(1/3.)
            term2 = term*term1
            mu = E*exp(A*term1 + B*term2)
        elif method in self.tabular_data:
            mu = self.interpolate(T, method)
        return mu