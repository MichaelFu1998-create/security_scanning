def does_not_contain_value(self, *values):
        """Asserts that val is a dict and does not contain the given value or values."""
        self._check_dict_like(self.val, check_getitem=False)
        if len(values) == 0:
            raise ValueError('one or more value args must be given')
        else:
            found = []
            for v in values:
                if v in self.val.values():
                    found.append(v)
            if found:
                self._err('Expected <%s> to not contain values %s, but did contain %s.' % (self.val, self._fmt_items(values), self._fmt_items(found)))
        return self