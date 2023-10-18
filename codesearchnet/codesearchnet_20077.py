def extract(self, document, selector, debug_offset=''):
        """
        Try and convert matching Elements to unicode strings.

        If this fails, the selector evaluation probably already
        returned some string(s) of some sort, or boolean value,
        or int/float, so return that instead.
        """
        selected = self.select(document, selector)
        if selected is not None:

            if isinstance(selected, (list, tuple)):

                # FIXME: return None or return empty list?
                if not len(selected):
                    return

                return [self._extract_single(m) for m in selected]

            else:
                return self._extract_single(selected)

        # selector did not match anything
        else:
            if self.DEBUG:
                print(debug_offset, "selector did not match anything; return None")
            return None