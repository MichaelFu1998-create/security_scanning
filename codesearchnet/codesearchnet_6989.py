def mul(self):
        r'''Viscosity of the mixture in the liquid phase at its current
        temperature, pressure, and composition in units of [Pa*s].

        For calculation of this property at other temperatures and pressures,
        or specifying manually the method used to calculate it, and more - see
        the object oriented interface
        :obj:`thermo.viscosity.ViscosityLiquidMixture`; each Mixture instance
        creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=320).mul
        0.0005767262693751547
        '''
        return self.ViscosityLiquidMixture(self.T, self.P, self.zs, self.ws)