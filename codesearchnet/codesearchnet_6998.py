def rhol_STP(self):
        r'''Liquid-phase mass density of the mixture at 298.15 K and 101.325 kPa,
        and the current composition in units of [kg/m^3].

        Examples
        --------
        >>> Mixture(['cyclobutane'], ws=[1]).rhol_STP
        688.9851989526821
        '''
        Vml = self.Vml_STP
        if Vml:
            return Vm_to_rho(Vml, self.MW)
        return None