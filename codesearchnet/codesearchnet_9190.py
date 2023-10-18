def setup(self, colormode=None, colorpalette=None, extend_colors=False):
        """
        Setup this colorful object by setting a ``colormode`` and
        the ``colorpalette`. The ``extend_colors`` flag is used
        to extend the currently active color palette instead of
        replacing it.

        :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
        :parma dict colorpalette: the colorpalette to use. This ``dict`` should map
                                  color names to it's corresponding RGB value
        :param bool extend_colors: extend the active color palette instead of replacing it
        """
        if colormode:
            self.colormode = colormode

        if colorpalette:
            if extend_colors:
                self.update_palette(colorpalette)
            else:
                self.colorpalette = colorpalette