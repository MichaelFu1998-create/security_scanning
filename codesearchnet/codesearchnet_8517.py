def contains_entry(self, *args, **kwargs):
        """Asserts that val is a dict and contains the given entry or entries."""
        self._check_dict_like(self.val, check_values=False)
        entries = list(args) + [{k:v} for k,v in kwargs.items()]
        if len(entries) == 0:
            raise ValueError('one or more entry args must be given')
        missing = []
        for e in entries:
            if type(e) is not dict:
                raise TypeError('given entry arg must be a dict')
            if len(e) != 1:
                raise ValueError('given entry args must contain exactly one key-value pair')
            k = next(iter(e))
            if k not in self.val:
                missing.append(e) # bad key
            elif self.val[k] != e[k]:
                missing.append(e) # bad val
        if missing:
            self._err('Expected <%s> to contain entries %s, but did not contain %s.' % (self.val, self._fmt_items(entries), self._fmt_items(missing)))
        return self