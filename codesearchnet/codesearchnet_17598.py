def H(self, H):
        """
        Set the enthalpy of the package to the specified value, and
        recalculate it's temperature.

        :param H: The new enthalpy value. [kWh]
        """

        self._H = H
        self._T = self._calculate_T(H)