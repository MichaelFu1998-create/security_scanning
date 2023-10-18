def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate thermal conductivity of a liquid mixture at 
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
        k : float
            Thermal conductivity of the liquid mixture, [W/m/K]
        '''
        if method == SIMPLE:
            ks = [i(T, P) for i in self.ThermalConductivityLiquids]
            return mixing_simple(zs, ks)
        elif method == DIPPR_9H:
            ks = [i(T, P) for i in self.ThermalConductivityLiquids]
            return DIPPR9H(ws, ks)
        elif method == FILIPPOV:
            ks = [i(T, P) for i in self.ThermalConductivityLiquids]
            return Filippov(ws, ks)
        elif method == MAGOMEDOV:
            k_w = self.ThermalConductivityLiquids[self.index_w](T, P)
            ws = list(ws) ; ws.pop(self.index_w)
            return thermal_conductivity_Magomedov(T, P, ws, self.wCASs, k_w)
        else:
            raise Exception('Method not valid')