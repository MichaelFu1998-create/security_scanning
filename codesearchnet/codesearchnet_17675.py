def S(self, T):
        """
        Calculate the portion of entropy of the compound phase covered by this
        Cp record.

        :param T: [K] temperature

        :returns: Entropy. [J/mol/K]
        """

        result = 0.0
        if T < self.Tmax:
            lT = T
        else:
            lT = self.Tmax
        Tref = self.Tmin
        for c, e in zip(self._coefficients, self._exponents):
            # Create a modified exponent to analytically integrate Cp(T)/T
            # instead of Cp(T).
            e_modified = e - 1.0
            if e_modified == -1.0:
                result += c * math.log(lT/Tref)
            else:
                e_mod = e_modified + 1.0
                result += c * (lT**e_mod - Tref**e_mod) / e_mod
        return result