def amount(self):
        """
        Determine the sum of mole amounts of all the compounds.

        :returns: Amount. [kmol]
        """

        return sum(self.get_compound_amount(c) for c in self.material.compounds)