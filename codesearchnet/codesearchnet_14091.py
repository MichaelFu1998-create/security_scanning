def _darkest(self):
        """
        Returns the darkest color from the list.

        Knowing the contrast between a light and a dark swatch
        can help us decide how to display readable typography.

        """
        min, n = (1.0, 1.0, 1.0), 3.0
        for clr in self:
            if clr.r + clr.g + clr.b < n:
                min, n = clr, clr.r + clr.g + clr.b

        return min