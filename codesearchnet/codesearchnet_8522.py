def is_named(self, filename):
        """Asserts that val is an existing path to a file and that file is named filename."""
        self.is_file()
        if not isinstance(filename, str_types):
            raise TypeError('given filename arg must be a path')
        val_filename = os.path.basename(os.path.abspath(self.val))
        if val_filename != filename:
            self._err('Expected filename <%s> to be equal to <%s>, but was not.' % (val_filename, filename))
        return self