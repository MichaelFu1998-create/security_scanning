def look(self, i=0):
        """ Look ahead of the iterable by some number of values with advancing
        past them.

        If the requested look ahead is past the end of the iterable then None is
        returned.

        """

        length = len(self.look_ahead)

        if length <= i:
            try:
                self.look_ahead.extend([next(self.iterable)
                    for _ in range(length, i + 1)])
            except StopIteration:
                return self.default

        self.value = self.look_ahead[i]
        return self.value