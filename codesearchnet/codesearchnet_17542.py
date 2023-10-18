def get_assay(self):
        """
        Determine the assay of self.

        :returns: [mass fractions] An array containing the assay of self.
        """

        masses_sum = sum(self.compound_masses)
        return [m / masses_sum for m in self.compound_masses]