def Cp(self, T):
        """
        Calculate the heat capacity of the compound phase.

        :param T: [K] temperature

        :returns: [J/mol/K] Heat capacity.
        """

        result = 0.0
        for c, e in zip(self._coefficients, self._exponents):
            result += c*T**e
        return result