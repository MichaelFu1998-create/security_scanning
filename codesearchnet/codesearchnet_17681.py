def S_mag(self, T):
        """
        Calculate the phase's magnetic contribution to entropy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The magnetic entropy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            s = 1 - (self._B_mag*(2*tau**3/3 + 2*tau**9/27 + 2*tau**15/75)) / \
                self._D_mag
        else:
            s = (2*tau**-5/5 + 2*tau**-15/45 + 2*tau**-25/125)/self._D_mag

        return -R*math.log(self.beta0_mag + 1)*s