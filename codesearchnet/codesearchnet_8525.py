def raises(self, ex):
        """Asserts that val is callable and that when called raises the given error."""
        if not callable(self.val):
            raise TypeError('val must be callable')
        if not issubclass(ex, BaseException):
            raise TypeError('given arg must be exception')
        return AssertionBuilder(self.val, self.description, self.kind, ex)