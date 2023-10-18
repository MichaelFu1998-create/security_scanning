def Cplm(self):
        r'''Liquid-phase heat capacity of the mixture at its current
        temperature and composition, in units of [J/mol/K]. For calculation of
        this property at other temperatures or compositions, or specifying
        manually the method used to calculate it, and more - see the object
        oriented interface :obj:`thermo.heat_capacity.HeatCapacityLiquidMixture`;
        each Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['toluene', 'decane'], ws=[.9, .1], T=300).Cplm
        168.29127923518843
        '''
        return self.HeatCapacityLiquidMixture(self.T, self.P, self.zs, self.ws)