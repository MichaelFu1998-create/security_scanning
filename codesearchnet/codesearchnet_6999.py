def rhog_STP(self):
        r'''Gas-phase mass density of the mixture at 298.15 K and 101.325 kPa,
        and the current composition in units of [kg/m^3].

        Examples
        --------
        >>> Mixture(['nitrogen'], ws=[1]).rhog_STP
        1.145534453639403
        '''
        Vmg = self.Vmg_STP
        if Vmg:
            return Vm_to_rho(Vmg, self.MW)
        return None