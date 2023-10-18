def isentropic_exponent(self):
        r'''Gas-phase ideal-gas isentropic exponent of the chemical at its
        current temperature, [dimensionless]. Does not include
        pressure-compensation from an equation of state.

        Examples
        --------
        >>> Chemical('hydrogen').isentropic_exponent
        1.405237786321222
        '''
        Cp, Cv = self.Cpg, self.Cvg
        if all((Cp, Cv)):
            return isentropic_exponent(Cp, Cv)
        return None