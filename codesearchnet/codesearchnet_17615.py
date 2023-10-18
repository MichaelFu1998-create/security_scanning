def Hfr(self, Hfr):
        """
        Set the enthalpy flow rate of the stream to the specified value, and
        recalculate it's temperature.

        :param H: The new enthalpy flow rate value. [kWh/h]
        """

        self._Hfr = Hfr
        self._T = self._calculate_T(Hfr)