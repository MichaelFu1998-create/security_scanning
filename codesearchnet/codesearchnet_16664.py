def cur_space(self, name=None):
        """Set the current space to Space ``name`` and return it.

        If called without arguments, the current space is returned.
        Otherwise, the current space is set to the space named ``name``
        and the space is returned.
        """
        if name is None:
            return self._impl.model.currentspace.interface
        else:
            self._impl.model.currentspace = self._impl.spaces[name]
            return self.cur_space()