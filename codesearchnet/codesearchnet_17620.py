def get_compound_mfr(self, compound):
        """
        Determine the mass flow rate of the specified compound in the stream.

        :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]".

        :returns: Mass flow rate. [kg/h]
        """

        if compound in self.material.compounds:
            return self._compound_mfrs[
                self.material.get_compound_index(compound)]
        else:
            return 0.0