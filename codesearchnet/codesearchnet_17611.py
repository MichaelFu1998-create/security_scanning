def _calculate_DH298_coal(self):
        """
        Calculate the enthalpy of formation of the dry-ash-free (daf) component of the coal.

        :returns: [kWh/kg daf] enthalpy of formation of daf coal
        """

        m_C = 0  # kg
        m_H = 0  # kg
        m_O = 0  # kg
        m_N = 0  # kg
        m_S = 0  # kg

        T = 25  # °C
        Hin = 0.0  # kWh
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            formula = compound.split('[')[0]
            if stoich.element_mass_fraction(formula, 'C') == 1.0:
                m_C += self._compound_mfrs[index]
                Hin += thermo.H(compound, T, self._compound_mfrs[index])
            elif stoich.element_mass_fraction(formula, 'H') == 1.0:
                m_H += self._compound_mfrs[index]
                Hin += thermo.H(compound, T, self._compound_mfrs[index])
            elif stoich.element_mass_fraction(formula, 'O') == 1.0:
                m_O += self._compound_mfrs[index]
                Hin += thermo.H(compound, T, self._compound_mfrs[index])
            elif stoich.element_mass_fraction(formula, 'N') == 1.0:
                m_N += self._compound_mfrs[index]
                Hin += thermo.H(compound, T, self._compound_mfrs[index])
            elif stoich.element_mass_fraction(formula, 'S') == 1.0:
                m_S += self._compound_mfrs[index]
                Hin += thermo.H(compound, T, self._compound_mfrs[index])

        m_total = m_C + m_H + m_O + m_N + m_S  # kg

        Hout = 0.0  # kWh
        Hout += thermo.H('CO2[G]', T, cc(m_C, 'C', 'CO2', 'C'))
        Hout += thermo.H('H2O[L]', T, cc(m_H, 'H', 'H2O', 'H'))
        Hout += thermo.H('O2[G]', T, m_O)
        Hout += thermo.H('N2[G]', T, m_N)
        Hout += thermo.H('SO2[G]', T, cc(m_S, 'S', 'SO2', 'S'))
        Hout /= m_total

        if self.HHV is None:
            # If no HHV is specified, calculate it from the proximate assay
            # using C-H-O-N-S.
            HHV = (Hout - Hin) / m_total  # kWh/kg daf
        else:
            # If an HHV is specified, convert it from MJ/kg coal to kWh/kg daf.
            HHV = self.HHV / 3.6  # kWh/kg coal
            HHV *= self.mfr / m_total  # kWh/kg daf

        return HHV + Hout