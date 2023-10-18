def _generateFindR(self, **kwargs):
        """Generator which yields matches on AXChildren and their children."""
        for needle in self._generateChildrenR():
            if needle._match(**kwargs):
                yield needle