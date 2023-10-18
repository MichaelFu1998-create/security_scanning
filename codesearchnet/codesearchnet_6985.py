def Cvgm(self):
        r'''Gas-phase ideal-gas contant-volume heat capacity of the mixture at
        its current temperature and composition, in units of [J/mol/K]. Subtracts R from
        the ideal-gas heat capacity; does not include pressure-compensation
        from an equation of state.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=520).Cvgm
        27.13366316134193
        '''
        Cpgm = self.HeatCapacityGasMixture(self.T, self.P, self.zs, self.ws)
        if Cpgm:
            return Cpgm - R
        return None