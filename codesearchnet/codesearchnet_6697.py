def Cvg(self):
        r'''Gas-phase ideal-gas contant-volume heat capacity of the chemical at
        its current temperature, in units of [J/kg/K]. Subtracts R from
        the ideal-gas heat capacity; does not include pressure-compensation
        from an equation of state.

        Examples
        --------
        >>> w = Chemical('water', T=520)
        >>> w.Cvg
        1506.1471795798861
        '''
        Cvgm = self.Cvgm
        if Cvgm:
            return property_molar_to_mass(Cvgm, self.MW)
        return None