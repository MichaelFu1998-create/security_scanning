def calculate(self, T, method):
        r'''Method to calculate permittivity of a liquid at temperature `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate relative permittivity, [K]
        method : str
            Name of the method to use

        Returns
        -------
        epsilon : float
            Relative permittivity of the liquid at T, [-]
        '''
        if method == CRC:
            A, B, C, D = self.CRC_coeffs
            epsilon = A + B*T + C*T**2 + D*T**3
        elif method == CRC_CONSTANT:
            epsilon = self.CRC_permittivity
        elif method in self.tabular_data:
            epsilon = self.interpolate(T, method)
        return epsilon