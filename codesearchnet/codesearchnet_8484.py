def is_instance_of(self, some_class):
        """Asserts that val is an instance of the given class."""
        try:
            if not isinstance(self.val, some_class):
                if hasattr(self.val, '__name__'):
                    t = self.val.__name__
                elif hasattr(self.val, '__class__'):
                    t = self.val.__class__.__name__
                else:
                    t = 'unknown'
                self._err('Expected <%s:%s> to be instance of class <%s>, but was not.' % (self.val, t, some_class.__name__))
        except TypeError:
            raise TypeError('given arg must be a class')
        return self