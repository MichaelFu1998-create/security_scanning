def _calculate_H(self, T):
        """
        Calculate the enthalpy of the package at the specified temperature.

        :param T: Temperature. [°C]

        :returns: Enthalpy. [kWh]
        """

        if self.isCoal:
            return self._calculate_Hfr_coal(T)

        H = 0.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            dH = thermo.H(compound, T, self._compound_masses[index])
            H = H + dH
        return H