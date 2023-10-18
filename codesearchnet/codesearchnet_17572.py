def clone(self):
        """
        Create a complete copy of self.

        :returns: A MaterialPackage that is identical to self.
        """

        result = copy.copy(self)
        result.size_class_masses = copy.deepcopy(self.size_class_masses)
        return result