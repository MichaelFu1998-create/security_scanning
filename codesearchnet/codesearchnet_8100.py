def clear(self):
        """Clear description to default values"""
        self._desc = {}
        for key, value in merge.DEFAULT_PROJECT.items():
            if key not in self._HIDDEN:
                self._desc[key] = type(value)()