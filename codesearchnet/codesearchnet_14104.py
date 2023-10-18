def contains(self, clr):
        """
        Returns True if the given color is part of this color range.

        Check whether each h, s, b, a component of the color
        falls within the defined range for that component.

        If the given color is grayscale,
        checks against the definitions for black and white.
        """
        if not isinstance(clr, Color):
            return False

        if not isinstance(clr, _list):
            clr = [clr]

        for clr in clr:

            if clr.is_grey and not self.grayscale:
                return (self.black.contains(clr) or \
                        self.white.contains(clr))

            for r, v in [(self.h, clr.h), (self.s, clr.s), (self.b, clr.brightness), (self.a, clr.a)]:
                if isinstance(r, _list):
                    pass
                elif isinstance(r, tuple):
                    r = [r]
                else:
                    r = [(r, r)]
                for min, max in r:
                    if not (min <= v <= max):
                        return False

        return True