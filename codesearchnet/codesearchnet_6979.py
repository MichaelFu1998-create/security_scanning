def Cpsm(self):
        r'''Solid-phase heat capacity of the mixture at its current temperature
        and composition, in units of [J/mol/K]. For calculation of this property
        at other temperatures or compositions, or specifying manually the
        method used to calculate it, and more - see the object oriented
        interface :obj:`thermo.heat_capacity.HeatCapacitySolidMixture`; each
        Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['silver', 'platinum'], ws=[0.95, 0.05]).Cpsm
        25.32745796347474
        '''
        return self.HeatCapacitySolidMixture(self.T, self.P, self.zs, self.ws)