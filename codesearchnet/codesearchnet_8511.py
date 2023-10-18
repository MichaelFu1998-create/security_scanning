def is_unicode(self):
        """Asserts that val is a unicode string."""
        if type(self.val) is not unicode:
            self._err('Expected <%s> to be unicode, but was <%s>.' % (self.val, type(self.val).__name__))
        return self