def _smixins(self, name):
        """Inner wrapper to search for mixins by name.
        """
        return (self._mixins[name] if name in self._mixins else False)