def set_colors_in_grid(self, some_colors_in_grid):
        """Same as :meth:`set_color_in_grid` but with a collection of
        colors in grid.

        :param iterable some_colors_in_grid: a collection of colors in grid for
          :meth:`set_color_in_grid`
        """
        for color_in_grid in some_colors_in_grid:
            self._set_pixel_and_convert_color(
                color_in_grid.x, color_in_grid.y, color_in_grid.color)