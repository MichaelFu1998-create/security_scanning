def Cp_mag(self, T):
        """
        Calculate the phase's magnetic contribution to heat capacity at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The magnetic heat capacity of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            c = (self._B_mag*(2*tau**3 + 2*tau**9/3 + 2*tau**15/5))/self._D_mag
        else:
            c = (2*tau**-5 + 2*tau**-15/3 + 2*tau**-25/5)/self._D_mag

        result = R*math.log(self.beta0_mag + 1)*c

        return result