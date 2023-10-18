def _cache(self):
        """
        Populates the list with a number of gradient colors.

        The list has Gradient.steps colors that interpolate between
        the fixed base Gradient.colors.

        The spread parameter controls the midpoint of the gradient,
        you can shift it right and left. A separate gradient is
        calculated for each half and then glued together.
        """
        n = self.steps

        # Only one color in base list.
        if len(self._colors) == 1:
            ColorList.__init__(self, [self._colors[0] for i in _range(n)])
            return

        # Expand the base list so we can chop more accurately.
        colors = self._interpolate(self._colors, 40)

        # Chop into left half and right half.
        # Make sure their ending and beginning match colors.
        left = colors[:len(colors) / 2]
        right = colors[len(colors) / 2:]
        left.append(right[0])
        right.insert(0, left[-1])

        # Calculate left and right gradient proportionally to spread.
        gradient = self._interpolate(left, int(n * self.spread))[:-1]
        gradient.extend(
            self._interpolate(right, n - int(n * self.spread))[1:]
        )

        if self.spread > 1: gradient = gradient[:n]
        if self.spread < 0: gradient = gradient[-n:]
        ColorList.__init__(self, gradient)