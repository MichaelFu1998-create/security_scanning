def points(self, amount=100, start=0.0, end=1.0, segments=None):
        """ Returns an iterator with a list of calculated points for the path.
            To omit the last point on closed paths: end=1-1.0/amount
        """
        # Originally from nodebox-gl
        if len(self._elements) == 0:
            raise PathError("The given path is empty")
        n = end - start
        d = n
        if amount > 1:
            # The delta value is divided by amount-1, because we also want the last point (t=1.0)
            # If we don't use amount-1, we fall one point short of the end.
            # If amount=4, we want the point at t 0.0, 0.33, 0.66 and 1.0.
            # If amount=2, we want the point at t 0.0 and 1.0.
            d = float(n) / (amount - 1)
        for i in xrange(int(amount)):
            yield self.point(start + d * i, segments)