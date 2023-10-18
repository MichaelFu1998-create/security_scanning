def append(self, item):
        """
        Append to object, if object is list.
        """
        if self.meta_type == 'dict':
            raise AssertionError('Cannot append to object of `dict` base type!')
        if self.meta_type == 'list':
            self._list.append(item)
        return