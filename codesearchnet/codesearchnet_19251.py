def first(self, symbols):
        """Computes the intermediate FIRST set using symbols."""
        ret = set()

        if EPSILON in symbols:
            return set([EPSILON])

        for symbol in symbols:
            ret |= self._first[symbol] - set([EPSILON])
            if EPSILON not in self._first[symbol]:
                break
        else:
            ret.add(EPSILON)

        return ret