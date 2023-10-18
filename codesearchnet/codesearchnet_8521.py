def is_directory(self):
        """Asserts that val is an existing path to a directory."""
        self.exists()
        if not os.path.isdir(self.val):
            self._err('Expected <%s> to be a directory, but was not.' % self.val)
        return self