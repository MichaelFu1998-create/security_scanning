def compile(self):
        """
        Build the abstract Parsley tree starting from the root node
        (recursive)
        """
        if not isinstance(self.parselet, dict):
            raise ValueError("Parselet must be a dict of some sort. Or use .from_jsonstring(), " \
                ".from_jsonfile(), .from_yamlstring(), or .from_yamlfile()")
        self.parselet_tree = self._compile(self.parselet)