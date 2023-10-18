def values(self):
        """
        Return keys for object, if they are available.
        """
        if self.meta_type == 'list':
            return self._list
        elif self.meta_type == 'dict':
            return self._dict.values()