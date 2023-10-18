def get_compound_amount(self, compound):
        """
        Determine the mole amount of the specified compound.

        :returns: Amount. [kmol]
        """

        index = self.material.get_compound_index(compound)
        return stoich.amount(compound, self._compound_masses[index])