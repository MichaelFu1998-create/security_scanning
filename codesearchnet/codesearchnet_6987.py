def Vmg(self):
        r'''Gas-phase molar volume of the mixture at its current
        temperature, pressure, and composition in units of [m^3/mol]. For
        calculation of this property at other temperatures or pressures or
        compositions, or specifying manually the method used to calculate it,
        and more - see the object oriented interface
        :obj:`thermo.volume.VolumeGasMixture`; each Mixture instance
        creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['hexane'], ws=[1], T=300, P=2E5).Vmg
        0.010888694235142216
        '''
        return self.VolumeGasMixture(T=self.T, P=self.P, zs=self.zs, ws=self.ws)