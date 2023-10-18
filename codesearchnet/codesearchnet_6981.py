def Cpgm(self):
        r'''Gas-phase heat capacity of the mixture at its current temperature
        and composition, in units of [J/mol/K]. For calculation of this property
        at other temperatures or compositions, or specifying manually the
        method used to calculate it, and more - see the object oriented
        interface :obj:`thermo.heat_capacity.HeatCapacityGasMixture`; each
        Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['oxygen', 'nitrogen'], ws=[.4, .6], T=350, P=1E6).Cpgm
        29.361044582498046
        '''
        return self.HeatCapacityGasMixture(self.T, self.P, self.zs, self.ws)