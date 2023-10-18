def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate viscosity of a liquid mixture at 
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
            Viscosity of the liquid mixture, [Pa*s]
        '''
        if method == MIXING_LOG_MOLAR:
            mus = [i(T, P) for i in self.ViscosityLiquids]
            return mixing_logarithmic(zs, mus)
        elif method == MIXING_LOG_MASS:
            mus = [i(T, P) for i in self.ViscosityLiquids]
            return mixing_logarithmic(ws, mus)
        elif method == LALIBERTE_MU:
            ws = list(ws) ; ws.pop(self.index_w)
            return Laliberte_viscosity(T, ws, self.wCASs)
        else:
            raise Exception('Method not valid')