def _findAllR(self, **kwargs):
        """Return a list of all children (recursively) that match the specified
        criteria.
        """
        result = []
        for item in self._generateFindR(**kwargs):
            result.append(item)
        return result