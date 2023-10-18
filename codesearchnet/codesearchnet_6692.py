def Hvap(self):
        r'''Enthalpy of vaporization of the chemical at its current temperature,
        in units of [J/kg].

        This property uses the object-oriented interface
        :obj:`thermo.phase_change.EnthalpyVaporization`, but converts its
        results from molar to mass units.

        Examples
        --------
        >>> Chemical('water', T=320).Hvap
        2389540.219347256
        '''
        Hvamp = self.Hvapm
        if Hvamp:
            return property_molar_to_mass(Hvamp, self.MW)
        return None