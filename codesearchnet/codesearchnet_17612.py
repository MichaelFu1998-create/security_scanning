def _calculate_Hfr_coal(self, T):
        """
        Calculate the enthalpy flow rate of the stream at the specified
        temperature, in the case of it being coal.

        :param T: Temperature. [°C]

        :returns: Enthalpy flow rate. [kWh/h]
        """

        m_C = 0  # kg/h
        m_H = 0  # kg/h
        m_O = 0  # kg/h
        m_N = 0  # kg/h
        m_S = 0  # kg/h

        Hfr = 0.0  # kWh/h
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            formula = compound.split('[')[0]
            if stoich.element_mass_fraction(formula, 'C') == 1.0:
                m_C += self._compound_mfrs[index]
            elif stoich.element_mass_fraction(formula, 'H') == 1.0:
                m_H += self._compound_mfrs[index]
            elif stoich.element_mass_fraction(formula, 'O') == 1.0:
                m_O += self._compound_mfrs[index]
            elif stoich.element_mass_fraction(formula, 'N') == 1.0:
                m_N += self._compound_mfrs[index]
            elif stoich.element_mass_fraction(formula, 'S') == 1.0:
                m_S += self._compound_mfrs[index]
            else:
                dHfr = thermo.H(compound, T, self._compound_mfrs[index])
                Hfr += dHfr

        m_total = m_C + m_H + m_O + m_N + m_S  # kg/h
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
        Hdaf *= m_total  # kWh/h

        Hfr += Hdaf

        return Hfr