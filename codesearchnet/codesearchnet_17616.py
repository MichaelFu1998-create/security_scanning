def T(self, T):
        """
        Set the temperature of the stream to the specified value, and
        recalculate it's enthalpy.

        :param T: Temperature. [°C]
        """

        self._T = T
        self._Hfr = self._calculate_Hfr(T)