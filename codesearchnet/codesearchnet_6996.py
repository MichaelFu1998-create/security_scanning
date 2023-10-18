def Vml_STP(self):
        r'''Liquid-phase molar volume of the mixture at 298.15 K and 101.325 kPa,
        and the current composition in units of [m^3/mol].

        Examples
        --------
        >>> Mixture(['cyclobutane'], ws=[1]).Vml_STP
        8.143327329133706e-05
        '''
        return self.VolumeLiquidMixture(T=298.15, P=101325, zs=self.zs, ws=self.ws)