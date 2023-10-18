def contains_only(self, *items):
        """Asserts that val contains only the given item or items."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        else:
            extra = []
            for i in self.val:
                if i not in items:
                    extra.append(i)
            if extra:
                self._err('Expected <%s> to contain only %s, but did contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(extra)))

            missing = []
            for i in items:
                if i not in self.val:
                    missing.append(i)
            if missing:
                self._err('Expected <%s> to contain only %s, but did not contain %s.' % (self.val, self._fmt_items(items), self._fmt_items(missing)))
        return self