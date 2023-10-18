def H(self, phase, T):
        """
        Calculate the enthalpy of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol] Enthalpy.
        """

        try:
            return self._phases[phase].H(T)
        except KeyError:
            raise Exception("The phase '{}' was not found in compound '{}'."
                            .format(phase, self.formula))