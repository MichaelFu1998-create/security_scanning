def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate heat capacity of a gas mixture at 
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
        Cpgm : float
            Molar heat capacity of the gas mixture at the given conditions,
            [J/mol]
        '''
        if method == SIMPLE:
            Cpgms = [i(T) for i in self.HeatCapacityGases]
            return mixing_simple(zs, Cpgms)
        else:
            raise Exception('Method not valid')