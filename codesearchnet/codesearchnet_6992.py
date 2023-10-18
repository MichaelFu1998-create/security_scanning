def kl(self):
        r'''Thermal conductivity of the mixture in the liquid phase at its current
        temperature, pressure, and composition in units of [Pa*s].

        For calculation of this property at other temperatures and pressures,
        or specifying manually the method used to calculate it, and more - see
        the object oriented interface
        :obj:`thermo.thermal_conductivity.ThermalConductivityLiquidMixture`;
        each Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=320).kl
        0.6369957248212118
        '''
        return self.ThermalConductivityLiquidMixture(self.T, self.P, self.zs, self.ws)