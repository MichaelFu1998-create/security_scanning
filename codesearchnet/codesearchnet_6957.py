def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate viscosity of a gas mixture at 
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
        mu : float
            Viscosity of gas mixture, [Pa*s]
        '''
        if method == SIMPLE:
            mus = [i(T, P) for i in self.ViscosityGases]
            return mixing_simple(zs, mus)
        elif method == HERNING_ZIPPERER:
            mus = [i(T, P) for i in self.ViscosityGases]
            return Herning_Zipperer(zs, mus, self.MWs)
        elif method == WILKE:
            mus = [i(T, P) for i in self.ViscosityGases]
            return Wilke(zs, mus, self.MWs)
        elif method == BROKAW:
            mus = [i(T, P) for i in self.ViscosityGases]
            return Brokaw(T, zs, mus, self.MWs, self.molecular_diameters, self.Stockmayers)
        else:
            raise Exception('Method not valid')