def _calculate_Hfr(self, T):
        """
        Calculate the enthalpy flow rate of the stream at the specified
        temperature.

        :param T: Temperature. [°C]

        :returns: Enthalpy flow rate. [kWh/h]
        """

        if self.isCoal:
            return self._calculate_Hfr_coal(T)

        Hfr = 0.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            dHfr = thermo.H(compound, T, self._compound_mfrs[index])
            Hfr = Hfr + dHfr
        return Hfr