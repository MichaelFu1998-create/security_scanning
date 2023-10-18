def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate surface tension of a liquid mixture at 
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
        sigma : float
            Surface tension of the liquid at given conditions, [N/m]
        '''
        if method == SIMPLE:
            sigmas = [i(T) for i in self.SurfaceTensions]
            return mixing_simple(zs, sigmas)
        elif method == DIGUILIOTEJA:
            return Diguilio_Teja(T=T, xs=zs, sigmas_Tb=self.sigmas_Tb, 
                                 Tbs=self.Tbs, Tcs=self.Tcs)
        elif method == WINTERFELDSCRIVENDAVIS:
            sigmas = [i(T) for i in self.SurfaceTensions]
            rhoms = [1./i(T, P) for i in self.VolumeLiquids]
            return Winterfeld_Scriven_Davis(zs, sigmas, rhoms)
        else:
            raise Exception('Method not valid')