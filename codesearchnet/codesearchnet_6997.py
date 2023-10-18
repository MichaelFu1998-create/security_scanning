def Vmg_STP(self):
        r'''Gas-phase molar volume of the mixture at 298.15 K and 101.325 kPa,
        and the current composition in units of [m^3/mol].

        Examples
        --------
        >>> Mixture(['nitrogen'], ws=[1]).Vmg_STP
        0.02445443688838904
        '''
        return self.VolumeGasMixture(T=298.15, P=101325, zs=self.zs, ws=self.ws)