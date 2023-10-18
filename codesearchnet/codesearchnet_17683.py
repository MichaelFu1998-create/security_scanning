def G_mag(self, T):
        """
        Calculate the phase's magnetic contribution to Gibbs energy at the
        specified temperature.

        :param T: [K] temperature

        :returns: [J/mol] The magnetic Gibbs energy of the compound phase.

        Dinsdale, A. T. (1991). SGTE data for pure elements. Calphad, 15(4),
        317–425. http://doi.org/10.1016/0364-5916(91)90030-N
        """

        tau = T / self.Tc_mag

        if tau <= 1.0:
            g = 1 - (self._A_mag/tau +
                     self._B_mag*(tau**3/6 + tau**9/135 + tau**15/600)) /\
                    self._D_mag
        else:
            g = -(tau**-5/10 + tau**-15/315 + tau**-25/1500)/self._D_mag

        return R*T*math.log(self.beta0_mag + 1)*g