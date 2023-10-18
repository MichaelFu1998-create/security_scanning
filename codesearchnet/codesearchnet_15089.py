def set_pixel(self, x, y, color):
        """set the pixel at ``(x, y)`` position to :paramref:`color`

        If ``(x, y)`` is out of the :ref:`bounds <png-builder-bounds>`
        this does not change the image.

        .. seealso:: :meth:`set_color_in_grid`
        """
        self._set_pixel_and_convert_color(x, y, color)