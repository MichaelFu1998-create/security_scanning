def calculate(self, T, method):
        r'''Method to calculate the molar volume of a solid at tempearture `T`
        with a given method.

        This method has no exception handling; see `T_dependent_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate molar volume, [K]
        method : str
            Name of the method to use

        Returns
        -------
        Vms : float
            Molar volume of the solid at T, [m^3/mol]
        '''
        if method == CRC_INORG_S:
            Vms = self.CRC_INORG_S_Vm
#        elif method == GOODMAN:
#            Vms = Goodman(T, self.Tt, self.rhol_Tt)
        elif method in self.tabular_data:
            Vms = self.interpolate(T, method)
        return Vms