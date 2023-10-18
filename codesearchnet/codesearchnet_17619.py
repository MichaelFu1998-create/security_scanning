def clear(self):
        """
        Set all the compound mass flow rates in the stream to zero.
        Set the pressure to 1, the temperature to 25 and the enthalpy to zero.
        """

        self._compound_mfrs = self._compound_mfrs * 0.0
        self._P = 1.0
        self._T = 25.0
        self._H = 0.0