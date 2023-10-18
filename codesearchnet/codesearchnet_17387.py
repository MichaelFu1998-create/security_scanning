def _generateChildren(self):
        """Generator which yields all AXChildren of the object."""
        try:
            children = self.AXChildren
        except _a11y.Error:
            return
        if children:
            for child in children:
                yield child