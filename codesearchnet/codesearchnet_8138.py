def get(self, position=0):
        """
        Return a color interpolated from the Palette.

        In the case where continuous=False, serpentine=False, scale=1,
        autoscale=False, and offset=0, this is exactly the same as plain old []
        indexing, but with a wrap-around.

        The constructor parameters affect this result as documented in the
        constructor.

        Arguments:
           ``position``:
             May be any integer or floating point number
        """
        n = len(self)
        if n == 1:
            return self[0]

        pos = position

        if self.length and self.autoscale:
            pos *= len(self)
            pos /= self.length

        pos *= self.scale
        pos += self.offset

        if not self.continuous:
            if not self.serpentine:
                return self[int(pos % n)]

            # We want a color sequence of length 2n-2
            # e.g. for n=5: a b c d | e d c b | a b c d ...
            m = (2 * n) - 2
            pos %= m
            if pos < n:
                return self[int(pos)]
            else:
                return self[int(m - pos)]

        if self.serpentine:
            pos %= (2 * n)
            if pos > n:
                pos = (2 * n) - pos
        else:
            pos %= n

        # p is a number in [0, n): scale it to be in [0, n-1)
        pos *= n - 1
        pos /= n

        index = int(pos)
        fade = pos - index
        if not fade:
            return self[index]

        r1, g1, b1 = self[index]
        r2, g2, b2 = self[(index + 1) % len(self)]
        dr, dg, db = r2 - r1, g2 - g1, b2 - b1

        return r1 + fade * dr, g1 + fade * dg, b1 + fade * db