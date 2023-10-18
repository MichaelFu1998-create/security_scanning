def _init_unique_sets(self):
        """Initialise sets used for uniqueness checking."""

        ks = dict()
        for t in self._unique_checks:
            key = t[0]
            ks[key] = set() # empty set
        return ks