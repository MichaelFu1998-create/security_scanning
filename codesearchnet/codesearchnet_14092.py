def _average(self):
        """
        Returns one average color for the colors in the list.
        """
        r, g, b, a = 0, 0, 0, 0
        for clr in self:
            r += clr.r
            g += clr.g
            b += clr.b
            a += clr.alpha

        r /= len(self)
        g /= len(self)
        b /= len(self)
        a /= len(self)

        return color(r, g, b, a, mode="rgb")