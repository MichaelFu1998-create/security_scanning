def load_pool(self):
        """
        Loads all the data files using the configured finders.
        """
        for meta in self._resources:
            resource = self.load(meta)
            yield meta, resource

        self._resources = []