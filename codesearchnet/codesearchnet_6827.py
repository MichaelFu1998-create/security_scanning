def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate molar volume of a solid mixture at 
        temperature `T`, pressure `P`, mole fractions `zs` and weight fractions
        `ws` with a given method.

        This method has no exception handling; see `mixture_property`
        for that.

        Parameters
        ----------
        T : float
            Temperature at which to calculate the property, [K]
        P : float
            Pressure at which to calculate the property, [Pa]
        zs : list[float]
            Mole fractions of all species in the mixture, [-]
        ws : list[float]
            Weight fractions of all species in the mixture, [-]
        method : str
            Name of the method to use

        Returns
        -------
        Vm : float
            Molar volume of the solid mixture at the given conditions,
            [m^3/mol]
        '''
        if method == SIMPLE:
            Vms = [i(T, P) for i in self.VolumeSolids]
            return mixing_simple(zs, Vms)
        else:
            raise Exception('Method not valid')