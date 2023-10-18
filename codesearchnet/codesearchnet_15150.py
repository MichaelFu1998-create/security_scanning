def insert_defs(self, defs):
        """Adds the defs to the SVG structure.

        :param defs: a list of SVG dictionaries, which contain the defs,
          which should be added to the SVG structure.
        """
        if self._svg["defs"] is None:
            self._svg["defs"] = {}
        for def_ in defs:
            for key, value in def_.items():
                if key.startswith("@"):
                    continue
                if key not in self._svg["defs"]:
                    self._svg["defs"][key] = []
                if not isinstance(value, list):
                    value = [value]
                self._svg["defs"][key].extend(value)