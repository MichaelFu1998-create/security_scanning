def clone(self):
        """Create a complete copy of the package.

        :returns: A new MaterialPackage object."""

        result = copy.copy(self)
        result._compound_masses = copy.deepcopy(self._compound_masses)
        return result