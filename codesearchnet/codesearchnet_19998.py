def _lexsorted_specs(self, order):
        """
        A lexsort is specified using normal key string prefixed by '+'
        (for ascending) or '-' for (for descending).

        Note that in Python 2, if a key is missing, None is returned
        (smallest Python value). In Python 3, an Exception will be
        raised regarding comparison of heterogenous types.
        """
        specs = self.specs[:]
        if not all(el[0] in ['+', '-'] for el in order):
            raise Exception("Please specify the keys for sorting, use"
                            "'+' prefix for ascending,"
                            "'-' for descending.)")

        sort_cycles = [(el[1:], True if el[0]=='+' else False)
                       for el in reversed(order)
                       if el[1:] in self.varying_keys]

        for (key, ascending) in sort_cycles:
            specs = sorted(specs, key=lambda s: s.get(key, None),
                           reverse=(not ascending))
        return specs