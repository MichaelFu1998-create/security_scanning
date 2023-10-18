def calculate(self, T, P, zs, ws, method):
        r'''Method to calculate molar volume of a gas mixture at 
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
            Molar volume of the gas mixture at the given conditions, [m^3/mol]
        '''
        if method == SIMPLE:
            Vms = [i(T, P) for i in self.VolumeGases]
            return mixing_simple(zs, Vms)
        elif method == IDEAL:
            return ideal_gas(T, P)
        elif method == EOS:
            self.eos[0] = self.eos[0].to_TP_zs(T=T, P=P, zs=zs)
            return self.eos[0].V_g
        else:
            raise Exception('Method not valid')