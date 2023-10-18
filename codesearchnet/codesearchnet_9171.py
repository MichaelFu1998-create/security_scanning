def with_setup(self, colormode=None, colorpalette=None, extend_colors=False):
        """
        Return a new Colorful object with the given color config.
        """
        colorful = Colorful(
            colormode=self.colorful.colormode,
            colorpalette=copy.copy(self.colorful.colorpalette)
        )

        colorful.setup(
            colormode=colormode, colorpalette=colorpalette, extend_colors=extend_colors
        )
        yield colorful