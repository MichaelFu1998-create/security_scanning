def Cps(self):
        r'''Solid-phase heat capacity of the mixture at its current temperature
        and composition, in units of [J/kg/K]. For calculation of this property
        at other temperatures or compositions, or specifying manually the
        method used to calculate it,  and more - see the object oriented
        interface :obj:`thermo.heat_capacity.HeatCapacitySolidMixture`; each
        Mixture instance creates one to actually perform the calculations. Note
        that that interface provides output in molar units.

        Examples
        --------
        >>> Mixture(['silver', 'platinum'], ws=[0.95, 0.05]).Cps
        229.55166388430328
        '''
        Cpsm = self.HeatCapacitySolidMixture(self.T, self.P, self.zs, self.ws)
        if Cpsm:
            return property_molar_to_mass(Cpsm, self.MW)
        return None