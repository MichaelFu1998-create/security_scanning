def extend(self, item):
        """
        Extend list from object, if object is list.
        """
        if self.meta_type == 'dict':
            raise AssertionError('Cannot extend to object of `dict` base type!')
        if self.meta_type == 'list':
            self._list.extend(item)
        return