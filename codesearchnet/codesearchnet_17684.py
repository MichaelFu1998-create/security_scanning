def Cp(self, phase, T):
        """
        Calculate the heat capacity of a phase of the compound at a specified
        temperature.

        :param phase: A phase of the compound, e.g. 'S', 'L', 'G'.
        :param T: [K] temperature

        :returns: [J/mol/K] Heat capacity.
        """

        if phase not in self._phases:
            raise Exception("The phase '%s' was not found in compound '%s'." %
                            (phase, self.formula))

        return self._phases[phase].Cp(T)