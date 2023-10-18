def does_not_contain(self, *items):
        """Asserts that val does not contain the given item or items."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        elif len(items) == 1:
            if items[0] in self.val:
                self._err('Expected <%s> to not contain item <%s>, but did.' % (self.val, items[0]))
        else:
            found = []
            for i in items:
                if i in self.val:
                    found.append(i)
            if found:
                self._err('Expected <%s> to not contain items %s, but did contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(found)))
        return self