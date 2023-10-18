def _data(self):
        """A simpler version of data to avoid infinite recursion in some cases.

        Don't use this.
        """
        if self.is_caching:
            return self.cache
        with open(self.path, "r") as f:
            return json.load(f)