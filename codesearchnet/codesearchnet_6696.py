def Cvgm(self):
        r'''Gas-phase ideal-gas contant-volume heat capacity of the chemical at
        its current temperature, in units of [J/mol/K]. Subtracts R from
        the ideal-gas heat capacity; does not include pressure-compensation
        from an equation of state.

        Examples
        --------
        >>> w = Chemical('water', T=520)
        >>> w.Cvgm
        27.13366316134193
        '''
        Cpgm = self.HeatCapacityGas(self.T)
        if Cpgm:
            return Cpgm - R
        return None