def _calculate_H_coal(self, T):
        """
        Calculate the enthalpy of the package at the specified temperature, in
        case the material is coal.

        :param T: [°C] temperature

        :returns: [kWh] enthalpy
        """

        m_C = 0  # kg
        m_H = 0  # kg
        m_O = 0  # kg
        m_N = 0  # kg
        m_S = 0  # kg

        H = 0.0  # kWh/h
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            if stoich.element_mass_fraction(compound, 'C') == 1.0:
                m_C += self._compound_masses[index]
            elif stoich.element_mass_fraction(compound, 'H') == 1.0:
                m_H += self._compound_masses[index]
            elif stoich.element_mass_fraction(compound, 'O') == 1.0:
                m_O += self._compound_masses[index]
            elif stoich.element_mass_fraction(compound, 'N') == 1.0:
                m_N += self._compound_masses[index]
            elif stoich.element_mass_fraction(compound, 'S') == 1.0:
                m_S += self._compound_masses[index]
            else:
                dH = thermo.H(compound, T, self._compound_masses[index])
                H += dH

        m_total = y_C + y_H + y_O + y_N + y_S  # kg/h
        y_C = m_C / m_total
        y_H = m_H / m_total
        y_O = m_O / m_total
        y_N = m_N / m_total
        y_S = m_S / m_total

        hmodel = coals.DafHTy()
        H = hmodel.calculate(T=T+273.15, y_C=y_C, y_H=y_H, y_O=y_O, y_N=y_N,
                             y_S=y_S) / 3.6e6  # kWh/kg
        H298 = hmodel.calculate(T=298.15, y_C=y_C, y_H=y_H, y_O=y_O, y_N=y_N,
                                y_S=y_S) / 3.6e6  # kWh/kg
        Hdaf = H - H298 + self._DH298  # kWh/kg
        Hdaf *= m_total  # kWh

        H += Hdaf

        return H