def calculate(self, **state):
        """
        Calculate the enthalpy at the specified temperature and composition
        using equation 9 in Merrick1983b.

        :param T: [K] temperature
        :param y_C: Carbon mass fraction
        :param y_H: Hydrogen mass fraction
        :param y_O: Oxygen mass fraction
        :param y_N: Nitrogen mass fraction
        :param y_S: Sulphur mass fraction

        :returns: [J/kg] enthalpy

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        T = state['T']
        y_C = state['y_C']
        y_H = state['y_H']
        y_O = state['y_O']
        y_N = state['y_N']
        y_S = state['y_S']

        a = self._calc_a(y_C, y_H, y_O, y_N, y_S) / 1000  # kg/mol
        result = (R/a) * (380*self._calc_g0(380/T) + 3600*self._calc_g0(1800/T))
        return result