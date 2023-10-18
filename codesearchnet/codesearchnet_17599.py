def T(self, T):
        """
        Set the temperature of the package to the specified value, and
        recalculate it's enthalpy.

        :param T: Temperature. [°C]
        """

        self._T = T
        self._H = self._calculate_H(T)