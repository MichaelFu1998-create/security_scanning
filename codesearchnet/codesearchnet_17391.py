def _generateFind(self, **kwargs):
        """Generator which yields matches on AXChildren."""
        for needle in self._generateChildren():
            if needle._match(**kwargs):
                yield needle