def is_child_of(self, parent):
        """Asserts that val is an existing path to a file and that file is a child of parent."""
        self.is_file()
        if not isinstance(parent, str_types):
            raise TypeError('given parent directory arg must be a path')
        val_abspath = os.path.abspath(self.val)
        parent_abspath = os.path.abspath(parent)
        if not val_abspath.startswith(parent_abspath):
            self._err('Expected file <%s> to be a child of <%s>, but was not.' % (val_abspath, parent_abspath))
        return self