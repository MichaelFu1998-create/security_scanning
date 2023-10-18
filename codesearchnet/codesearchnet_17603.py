def get_compound_amounts(self):
        """
        Determine the mole amounts of all the compounds.

        :returns: List of amounts. [kmol]
        """

        result = self._compound_masses * 1.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            result[index] = stoich.amount(compound, result[index])
        return result