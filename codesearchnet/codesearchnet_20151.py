def bind(self, module, prefs):
        """
        :param ModuleType module:
        :param list prefs: Preference names. Just to speed up __getattr__.
        """
        self._module = module
        self._prefs = set(prefs)