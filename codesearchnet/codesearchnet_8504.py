def starts_with(self, prefix):
        """Asserts that val is string or iterable and starts with prefix."""
        if prefix is None:
            raise TypeError('given prefix arg must not be none')
        if isinstance(self.val, str_types):
            if not isinstance(prefix, str_types):
                raise TypeError('given prefix arg must be a string')
            if len(prefix) == 0:
                raise ValueError('given prefix arg must not be empty')
            if not self.val.startswith(prefix):
                self._err('Expected <%s> to start with <%s>, but did not.' % (self.val, prefix))
        elif isinstance(self.val, Iterable):
            if len(self.val) == 0:
                raise ValueError('val must not be empty')
            first = next(iter(self.val))
            if first != prefix:
                self._err('Expected %s to start with <%s>, but did not.' % (self.val, prefix))
        else:
            raise TypeError('val is not a string or iterable')
        return self