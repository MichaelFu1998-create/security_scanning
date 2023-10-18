def ends_with(self, suffix):
        """Asserts that val is string or iterable and ends with suffix."""
        if suffix is None:
            raise TypeError('given suffix arg must not be none')
        if isinstance(self.val, str_types):
            if not isinstance(suffix, str_types):
                raise TypeError('given suffix arg must be a string')
            if len(suffix) == 0:
                raise ValueError('given suffix arg must not be empty')
            if not self.val.endswith(suffix):
                self._err('Expected <%s> to end with <%s>, but did not.' % (self.val, suffix))
        elif isinstance(self.val, Iterable):
            if len(self.val) == 0:
                raise ValueError('val must not be empty')
            last = None
            for last in self.val:
                pass
            if last != suffix:
                self._err('Expected %s to end with <%s>, but did not.' % (self.val, suffix))
        else:
            raise TypeError('val is not a string or iterable')
        return self