def H_mag(self, T):
        """
        Calculate the phase's magnetic contribution to enthalpy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol] The magnetic enthalpy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            h = (-self._A_mag/tau +
                 self._B_mag*(tau**3/2 + tau**9/15 + tau**15/40))/self._D_mag
        else:
            h = -(tau**-5/2 + tau**-15/21 + tau**-25/60)/self._D_mag

        return R*T*math.log(self.beta0_mag + 1)*h