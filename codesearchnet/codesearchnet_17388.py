def _generateChildrenR(self, target=None):
        """Generator which recursively yields all AXChildren of the object."""
        if target is None:
            target = self
        try:
            children = target.AXChildren
        except _a11y.Error:
            return
        if children:
            for child in children:
                yield child
                for c in self._generateChildrenR(child):
                    yield c