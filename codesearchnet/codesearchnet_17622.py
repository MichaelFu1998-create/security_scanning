def get_compound_afr(self, compound):
        """
        Determine the amount flow rate of the specified compound.

        :returns: Amount flow rate. [kmol/h]
        """

        index = self.material.get_compound_index(compound)
        return stoich.amount(compound, self._compound_mfrs[index])