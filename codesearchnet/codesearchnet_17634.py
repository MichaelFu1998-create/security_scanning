def calculate(self, **state):
        """
        Calculate the material physical property at the specified temperature
        in the units specified by the object's 'property_units' property.

        :param T: [K] temperature

        :returns: physical property value
        """
        super().calculate(**state)
        return np.polyval(self._coeffs, state['T'])