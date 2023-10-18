def update(self, other):
        """
        Update internal dictionary object. This is meant to be an
        analog for dict.update().
        """
        if self.meta_type == 'list':
            raise AssertionError('Cannot update object of `list` base type!')
        elif self.meta_type == 'dict':
            self._dict = dict(self + composite(other))
            return