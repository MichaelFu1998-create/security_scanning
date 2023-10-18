def is_less_than(self, other):
        """Asserts that val is numeric and is less than other."""
        self._validate_compareable(other)
        if self.val >= other:
            if type(self.val) is datetime.datetime:
                self._err('Expected <%s> to be less than <%s>, but was not.' % (self.val.strftime('%Y-%m-%d %H:%M:%S'), other.strftime('%Y-%m-%d %H:%M:%S')))
            else:
                self._err('Expected <%s> to be less than <%s>, but was not.' % (self.val, other))
        return self