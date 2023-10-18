def Cpg(self):
        r'''Gas-phase heat capacity of the mixture at its current temperature ,
        and composition in units of [J/kg/K]. For calculation of this property at
        other temperatures or compositions, or specifying manually the method
        used to calculate it, and more - see the object oriented interface
        :obj:`thermo.heat_capacity.HeatCapacityGasMixture`; each Mixture
        instance creates one to actually perform the calculations. Note that
        that interface provides output in molar units.

        Examples
        --------
        >>> Mixture(['oxygen', 'nitrogen'], ws=[.4, .6], T=350, P=1E6).Cpg
        995.8911053614883
        '''
        Cpgm = self.HeatCapacityGasMixture(self.T, self.P, self.zs, self.ws)
        if Cpgm:
            return property_molar_to_mass(Cpgm, self.MW)
        return None