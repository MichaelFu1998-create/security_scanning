def colorpalette(self, colorpalette):
        """
        Set the colorpalette which should be used
        """
        if isinstance(colorpalette, str):  # we assume it's a path to a color file
            colorpalette = colors.parse_colors(colorpalette)

        self._colorpalette = colors.sanitize_color_palette(colorpalette)