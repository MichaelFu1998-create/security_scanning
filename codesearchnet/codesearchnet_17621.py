def get_compound_afrs(self):
        """
        Determine the amount flow rates of all the compounds.

        :returns: List of amount flow rates. [kmol/h]
        """

        result = self._compound_mfrs * 1.0
        for compound in self.material.compounds:
            index = self.material.get_compound_index(compound)
            result[index] = stoich.amount(compound, result[index])
        return result