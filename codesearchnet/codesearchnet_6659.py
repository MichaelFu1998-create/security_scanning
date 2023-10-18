def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate heat capacity of a liquid mixture at 
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
        Cplm : float
            Molar heat capacity of the liquid mixture at the given conditions,
            [J/mol]
        '''
        if method == SIMPLE:
            Cplms = [i(T) for i in self.HeatCapacityLiquids]
            return mixing_simple(zs, Cplms)
        elif method == LALIBERTE:
            ws = list(ws) ; ws.pop(self.index_w)
            Cpl = Laliberte_heat_capacity(T, ws, self.wCASs)
            MW = mixing_simple(zs, self.MWs)
            return property_mass_to_molar(Cpl, MW)
        else:
            raise Exception('Method not valid')