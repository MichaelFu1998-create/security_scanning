def S(self, T):
        """
        Calculate the entropy of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The entropy of the compound phase.
        """

        result = self.Sref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            result += self._Cp_records[str(Tmax)].S(T)
            if T <= Tmax:
                return result + self.S_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        result += self.Cp(Tmax)*math.log(T / Tmax)

        return result + self.S_mag(T)