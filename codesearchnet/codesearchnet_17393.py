def _findAll(self, **kwargs):
        """Return a list of all children that match the specified criteria."""
        result = []
        for item in self._generateFind(**kwargs):
            result.append(item)
        return result