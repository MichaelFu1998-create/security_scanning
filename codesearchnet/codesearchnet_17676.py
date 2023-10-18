def Cp(self, T):
        """
        Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol/K] The heat capacity of the compound phase.
        """

        # TODO: Fix str/float conversion
        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            if T < Tmax:
                return self._Cp_records[str(Tmax)].Cp(T) + self.Cp_mag(T)

        Tmax = max([float(TT) for TT in self._Cp_records.keys()])

        return self._Cp_records[str(Tmax)].Cp(Tmax) + self.Cp_mag(T)