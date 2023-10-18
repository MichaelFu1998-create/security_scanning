def Cpl(self):
        r'''Liquid-phase heat capacity of the mixture at its current
        temperature and composition, in units of [J/kg/K]. For calculation of
        this property at other temperatures or compositions, or specifying
        manually the method used to calculate it, and more - see the object
        oriented interface :obj:`thermo.heat_capacity.HeatCapacityLiquidMixture`;
        each Mixture instance creates one to actually perform the calculations.
        Note that that interface provides output in molar units.

        Examples
        --------
        >>> Mixture(['water', 'sodium chloride'], ws=[.9, .1], T=301.5).Cpl
        3735.4604049449786
        '''
        Cplm = self.HeatCapacityLiquidMixture(self.T, self.P, self.zs, self.ws)
        if Cplm:
            return property_molar_to_mass(Cplm, self.MW)
        return None