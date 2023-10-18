def H(self, T):
        """
        Calculate the portion of enthalpy of the compound phase covered by this
        Cp record.

        :param T: [K] temperature

        :returns: [J/mol] Enthalpy.
        """

        result = 0.0
        if T < self.Tmax:
            lT = T
        else:
            lT = self.Tmax
        Tref = self.Tmin

        for c, e in zip(self._coefficients, self._exponents):
            # Analytically integrate Cp(T).
            if e == -1.0:
                result += c * math.log(lT/Tref)
            else:
                result += c * (lT**(e+1.0) - Tref**(e+1.0)) / (e+1.0)
        return result