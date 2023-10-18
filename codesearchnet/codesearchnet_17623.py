def afr(self):
        """
        Determine the sum of amount flow rates of all the compounds.

        :returns: Amount flow rate. [kmol/h]
        """

        result = 0.0
        for compound in self.material.compounds:
            result += self.get_compound_afr(compound)
        return result