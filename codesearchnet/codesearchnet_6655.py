def calculate(self, T, method):
        r'''Method to calculate heat capacity of a solid at temperature `T`
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
            Heat capacity of the solid at T, [J/mol/K]
        '''
        if method == PERRY151:
            Cp = (self.PERRY151_const + self.PERRY151_lin*T
            + self.PERRY151_quadinv/T**2 + self.PERRY151_quad*T**2)*calorie
        elif method == CRCSTD:
            Cp = self.CRCSTD_Cp
        elif method == LASTOVKA_S:
            Cp = Lastovka_solid(T, self.similarity_variable)
            Cp = property_mass_to_molar(Cp, self.MW)
        elif method in self.tabular_data:
            Cp = self.interpolate(T, method)
        return Cp