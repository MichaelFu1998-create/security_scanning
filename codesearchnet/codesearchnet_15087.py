def _set_pixel_and_convert_color(self, x, y, color):
        """set the pixel but convert the color before."""
        if color is None:
            return
        color = self._convert_color_to_rrggbb(color)
        self._set_pixel(x, y, color)