def color(self, clr=None, d=0.035):
        """
        Returns a color with random values in the defined h, s b, a ranges.

        If a color is given, use that color's hue and alpha,
        and generate its saturation and brightness from the shade.
        The hue is varied with the given d.

        In this way you could have a "warm" color range
        that returns all kinds of warm colors.
        When a red color is given as parameter it would generate
        all kinds of warm red colors.
        """
        # Revert to grayscale for black, white and grey hues.
        if clr != None and not isinstance(clr, Color):
            clr = color(clr)
        if clr != None and not self.grayscale:
            if clr.is_black: return self.black.color(clr, d)
            if clr.is_white: return self.white.color(clr, d)
            if clr.is_grey: return choice(
                (self.black.color(clr, d), self.white.color(clr, d))
            )

        h, s, b, a = self.h, self.s, self.b, self.a
        if clr != None:
            h, a = clr.h + d * (random() * 2 - 1), clr.a

        hsba = []
        for v in [h, s, b, a]:
            if isinstance(v, _list):
                min, max = choice(v)
            elif isinstance(v, tuple):
                min, max = v
            else:
                min, max = v, v
            hsba.append(min + (max - min) * random())

        h, s, b, a = hsba
        return color(h, s, b, a, mode="hsb")