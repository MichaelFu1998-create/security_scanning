def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate molar volume of a liquid mixture at 
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
            Molar volume of the liquid mixture at the given conditions, 
            [m^3/mol]
        '''
        if method == SIMPLE:
            Vms = [i(T, P) for i in self.VolumeLiquids]
            return Amgat(zs, Vms)
        elif method == COSTALD_MIXTURE:
            return COSTALD_mixture(zs, T, self.Tcs, self.Vcs, self.omegas)
        elif method == COSTALD_MIXTURE_FIT:
            return COSTALD_mixture(zs, T, self.Tcs, self.COSTALD_Vchars, self.COSTALD_omegas)
        elif method == RACKETT:
            return Rackett_mixture(T, zs, self.MWs, self.Tcs, self.Pcs, self.Zcs)
        elif method == RACKETT_PARAMETERS:
            return Rackett_mixture(T, zs, self.MWs, self.Tcs, self.Pcs, self.Z_RAs)
        elif method == LALIBERTE:
            ws = list(ws) ; ws.pop(self.index_w)
            rho = Laliberte_density(T, ws, self.wCASs)
            MW = mixing_simple(zs, self.MWs)
            return rho_to_Vm(rho, MW)
        else:
            raise Exception('Method not valid')