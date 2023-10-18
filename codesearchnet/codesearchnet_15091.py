def set_color_in_grid(self, color_in_grid):
        """Set the pixel at the position of the :paramref:`color_in_grid`
        to its color.

        :param color_in_grid: must have the following attributes:

          - ``color`` is the :ref:`color <png-color>` to set the pixel to
          - ``x`` is the x position of the pixel
          - ``y`` is the y position of the pixel

        .. seealso:: :meth:`set_pixel`, :meth:`set_colors_in_grid`
        """
        self._set_pixel_and_convert_color(
            color_in_grid.x, color_in_grid.y, color_in_grid.color)