def contains_ignoring_case(self, *items):
        """Asserts that val is string and contains the given item or items."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        if isinstance(self.val, str_types):
            if len(items) == 1:
                if not isinstance(items[0], str_types):
                    raise TypeError('given arg must be a string')
                if items[0].lower() not in self.val.lower():
                    self._err('Expected <%s> to case-insensitive contain item <%s>, but did not.' % (self.val, items[0]))
            else:
                missing = []
                for i in items:
                    if not isinstance(i, str_types):
                        raise TypeError('given args must all be strings')
                    if i.lower() not in self.val.lower():
                        missing.append(i)
                if missing:
                    self._err('Expected <%s> to case-insensitive contain items %s, but did not contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(missing)))
        elif isinstance(self.val, Iterable):
            missing = []
            for i in items:
                if not isinstance(i, str_types):
                    raise TypeError('given args must all be strings')
                found = False
                for v in self.val:
                    if not isinstance(v, str_types):
                        raise TypeError('val items must all be strings')
                    if i.lower() == v.lower():
                        found = True
                        break
                if not found:
                    missing.append(i)
            if missing:
                self._err('Expected <%s> to case-insensitive contain items %s, but did not contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(missing)))
        else:
            raise TypeError('val is not a string or iterable')
        return self