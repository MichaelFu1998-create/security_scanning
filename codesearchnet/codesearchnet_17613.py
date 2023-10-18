def _calculate_T(self, Hfr):
        """
        Calculate the temperature of the stream given the specified
        enthalpy flow rate using a secant algorithm.

        :param H: Enthalpy flow rate. [kWh/h]

        :returns: Temperature. [°C]
        """

        # Create the initial guesses for temperature.
        x = list()
        x.append(self._T)
        x.append(self._T + 10.0)

        # Evaluate the enthalpy for the initial guesses.
        y = list()
        y.append(self._calculate_Hfr(x[0]) - Hfr)
        y.append(self._calculate_Hfr(x[1]) - Hfr)

        # Solve for temperature.
        for i in range(2, 50):
            x.append(x[i-1] - y[i-1]*((x[i-1] - x[i-2])/(y[i-1] - y[i-2])))
            y.append(self._calculate_Hfr(x[i]) - Hfr)
            if abs(y[i-1]) < 1.0e-5:
                break

        return x[len(x) - 1]