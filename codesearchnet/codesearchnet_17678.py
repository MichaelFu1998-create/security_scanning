def H(self, T):
        """
        Calculate the enthalpy of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol] The enthalpy of the compound phase.
        """

        result = self.DHref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            result += self._Cp_records[str(Tmax)].H(T)
            if T <= Tmax:
                return result + self.H_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        result += self.Cp(Tmax)*(T - Tmax)

        return result + self.H_mag(T)