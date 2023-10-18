def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate thermal conductivity of a gas mixture at 
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
        kg : float
            Thermal conductivity of gas mixture, [W/m/K]
        '''
        if method == SIMPLE:
            ks = [i(T, P) for i in self.ThermalConductivityGases]
            return mixing_simple(zs, ks)
        elif method == LINDSAY_BROMLEY:
            ks = [i(T, P) for i in self.ThermalConductivityGases]
            mus = [i(T, P) for i in self.ViscosityGases]
            return Lindsay_Bromley(T=T, ys=zs, ks=ks, mus=mus, Tbs=self.Tbs, MWs=self.MWs)
        else:
            raise Exception('Method not valid')