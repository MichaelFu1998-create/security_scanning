def is_between(self, low, high):
        """Asserts that val is numeric and is between low and high."""
        val_type = type(self.val)
        self._validate_between_args(val_type, low, high)

        if self.val < low or self.val > high:
            if val_type is datetime.datetime:
                self._err('Expected <%s> to be between <%s> and <%s>, but was not.' % (self.val.strftime('%Y-%m-%d %H:%M:%S'), low.strftime('%Y-%m-%d %H:%M:%S'), high.strftime('%Y-%m-%d %H:%M:%S')))
            else:
                self._err('Expected <%s> to be between <%s> and <%s>, but was not.' % (self.val, low, high))
        return self