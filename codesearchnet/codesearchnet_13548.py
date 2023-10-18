def _make_prefix(self, declared_prefixes):
        """Make up a new namespace prefix, which won't conflict
        with `_prefixes` and prefixes declared in the current scope.

        :Parameters:
            - `declared_prefixes`: namespace to prefix mapping for the current
              scope
        :Types:
            - `declared_prefixes`: `unicode` to `unicode` dictionary

        :Returns: a new prefix
        :Returntype: `unicode`
        """
        used_prefixes = set(self._prefixes.values())
        used_prefixes |= set(declared_prefixes.values())
        while True:
            prefix = u"ns{0}".format(self._next_id)
            self._next_id += 1
            if prefix not in used_prefixes:
                break
        return prefix