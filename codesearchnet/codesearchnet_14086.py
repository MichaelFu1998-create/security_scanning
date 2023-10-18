def swatch(self, x, y, w=35, h=35, roundness=0):
        """
        Rectangle swatch for this color.
        """
        _ctx.fill(self)
        _ctx.rect(x, y, w, h, roundness)