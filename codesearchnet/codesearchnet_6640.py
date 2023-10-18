def calculate(self, T, method):
        r'''Method to calculate surface tension of a liquid at temperature `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate heat capacity, [K]
        method : str
            Method name to use

        Returns
        -------
        Cp : float
            Calculated heat capacity, [J/mol/K]
        '''
        if method == TRCIG:
            Cp = TRCCp(T, *self.TRCIG_coefs)
        elif method == COOLPROP:
            Cp = PropsSI('Cp0molar', 'T', T,'P', 101325.0, self.CASRN)
        elif method == POLING:
            Cp = R*(self.POLING_coefs[0] + self.POLING_coefs[1]*T
            + self.POLING_coefs[2]*T**2 + self.POLING_coefs[3]*T**3
            + self.POLING_coefs[4]*T**4)
        elif method == POLING_CONST:
            Cp = self.POLING_constant
        elif method == CRCSTD:
            Cp = self.CRCSTD_constant
        elif method == LASTOVKA_SHAW:
            Cp = Lastovka_Shaw(T, self.similarity_variable)
            Cp = property_mass_to_molar(Cp, self.MW)
        elif method in self.tabular_data:
            Cp = self.interpolate(T, method)
        return Cp