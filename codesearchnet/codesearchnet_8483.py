def is_type_of(self, some_type):
        """Asserts that val is of the given type."""
        if type(some_type) is not type and\
                not issubclass(type(some_type), type):
            raise TypeError('given arg must be a type')
        if type(self.val) is not some_type:
            if hasattr(self.val, '__name__'):
                t = self.val.__name__
            elif hasattr(self.val, '__class__'):
                t = self.val.__class__.__name__
            else:
                t = 'unknown'
            self._err('Expected <%s:%s> to be of type <%s>, but was not.' % (self.val, t, some_type.__name__))
        return self