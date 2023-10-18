def get_compound_mass(self, compound):
        """
        Determine the mass of the specified compound in the package.

        :param compound: Formula and phase of a compound, e.g. "Fe2O3[S1]".

        :returns: Mass. [kg]
        """

        if compound in self.material.compounds:
            return self._compound_masses[
                self.material.get_compound_index(compound)]
        else:
            return 0.0