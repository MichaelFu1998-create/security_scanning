def swatch(self, x, y, w=35, h=35, padding=0, roundness=0):
        """
        Rectangle swatches for all the colors in the list.
        """
        for clr in self:
            clr.swatch(x, y, w, h, roundness)
            y += h + padding