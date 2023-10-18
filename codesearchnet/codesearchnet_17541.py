def clone(self):
        """
        Create a complete copy of self.

        :returns: A MaterialPackage that is identical to self.
        """

        result = copy.copy(self)
        result.compound_masses = copy.deepcopy(self.compound_masses)

        return result