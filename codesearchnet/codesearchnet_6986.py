def Vml(self):
        r'''Liquid-phase molar volume of the mixture at its current
        temperature, pressure, and composition in units of [m^3/mol]. For
        calculation of this property at other temperatures or pressures or
        compositions, or specifying manually the method used to calculate it,
        and more - see the object oriented interface
        :obj:`thermo.volume.VolumeLiquidMixture`; each Mixture instance
        creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['cyclobutane'], ws=[1], T=225).Vml
        7.42395423425395e-05
        '''
        return self.VolumeLiquidMixture(T=self.T, P=self.P, zs=self.zs, ws=self.ws)