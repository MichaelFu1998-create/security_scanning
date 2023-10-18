def contains(self, *items):
        """Asserts that val contains the given item or items."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        elif len(items) == 1:
            if items[0] not in self.val:
                if self._check_dict_like(self.val, return_as_bool=True):
                    self._err('Expected <%s> to contain key <%s>, but did not.' % (self.val, items[0]))
                else:
                    self._err('Expected <%s> to contain item <%s>, but did not.' % (self.val, items[0]))
        else:
            missing = []
            for i in items:
                if i not in self.val:
                    missing.append(i)
            if missing:
                if self._check_dict_like(self.val, return_as_bool=True):
                    self._err('Expected <%s> to contain keys %s, but did not contain key%s %s.' % (self.val, self._fmt_items(items), '' if len(missing) == 0 else 's', self._fmt_items(missing)))
                else:
                    self._err('Expected <%s> to contain items %s, but did not contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(missing)))
        return self