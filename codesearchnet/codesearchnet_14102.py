def copy(self, clr=None, d=0.0):
        """
        Returns a copy of the range.

        Optionally, supply a color to get a range copy
        limited to the hue of that color.
        """
        cr = ColorRange()
        cr.name = self.name

        cr.h = deepcopy(self.h)
        cr.s = deepcopy(self.s)
        cr.b = deepcopy(self.b)
        cr.a = deepcopy(self.a)

        cr.grayscale = self.grayscale
        if not self.grayscale:
            cr.black = self.black.copy()
            cr.white = self.white.copy()

        if clr != None:
            cr.h, cr.a = clr.h + d * (random() * 2 - 1), clr.a

        return cr