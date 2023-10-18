def calculate(self, T, method):
        r'''Method to calculate heat capacity of a liquid at temperature `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate heat capacity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Cp : float
            Heat capacity of the liquid at T, [J/mol/K]
        '''
        if method == ZABRANSKY_SPLINE:
            return self.Zabransky_spline.calculate(T)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL:
            return self.Zabransky_quasipolynomial.calculate(T)
        elif method == ZABRANSKY_SPLINE_C:
            return self.Zabransky_spline_iso.calculate(T)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_C:
            return self.Zabransky_quasipolynomial_iso.calculate(T)
        elif method == ZABRANSKY_SPLINE_SAT:
            return self.Zabransky_spline_sat.calculate(T)
        elif method == ZABRANSKY_QUASIPOLYNOMIAL_SAT:
            return self.Zabransky_quasipolynomial_sat.calculate(T)
        elif method == COOLPROP:
            return CoolProp_T_dependent_property(T, self.CASRN , 'CPMOLAR', 'l')
        elif method == POLING_CONST:
            return self.POLING_constant
        elif method == CRCSTD:
            return self.CRCSTD_constant
        elif method == ROWLINSON_POLING:
            Cpgm = self.Cpgm(T) if hasattr(self.Cpgm, '__call__') else self.Cpgm
            return Rowlinson_Poling(T, self.Tc, self.omega, Cpgm)
        elif method == ROWLINSON_BONDI:
            Cpgm = self.Cpgm(T) if hasattr(self.Cpgm, '__call__') else self.Cpgm
            return Rowlinson_Bondi(T, self.Tc, self.omega, Cpgm)
        elif method == DADGOSTAR_SHAW:
            Cp = Dadgostar_Shaw(T, self.similarity_variable)
            return property_mass_to_molar(Cp, self.MW)
        elif method in self.tabular_data:
            return self.interpolate(T, method)
        else:
            raise Exception('Method not valid')