def is_file(self):
        """Asserts that val is an existing path to a file."""
        self.exists()
        if not os.path.isfile(self.val):
            self._err('Expected <%s> to be a file, but was not.' % self.val)
        return self