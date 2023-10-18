def G(self, T):
        """Calculate the heat capacity of the compound phase at the specified
        temperature.

        :param T: [K] temperature

        :returns: [J/mol] The Gibbs free energy of the compound phase.
        """

        h = self.DHref
        s = self.Sref

        for Tmax in sorted([float(TT) for TT in self._Cp_records.keys()]):
            h = h + self._Cp_records[str(Tmax)].H(T)
            s = s + self._Cp_records[str(Tmax)].S(T)
            if T <= Tmax:
                return h - T * s + self.G_mag(T)

        # Extrapolate beyond the upper limit by using a constant heat capacity.
        Tmax = max([float(TT) for TT in self._Cp_records.keys()])
        h = h + self.Cp(Tmax)*(T - Tmax)
        s = s + self.Cp(Tmax)*math.log(T / Tmax)

        return h - T * s + self.G_mag(T)