def contains_value(self, *values):
        """Asserts that val is a dict and contains the given value or values."""
        self._check_dict_like(self.val, check_getitem=False)
        if len(values) == 0:
            raise ValueError('one or more value args must be given')
        missing = []
        for v in values:
            if v not in self.val.values():
                missing.append(v)
        if missing:
            self._err('Expected <%s> to contain values %s, but did not contain %s.' % (self.val, self._fmt_items(values), self._fmt_items(missing)))
        return self