def _set_pixel(self, x, y, color):
        """set the color of the pixel.

        :param color: must be a valid color in the form of "#RRGGBB".
          If you need to convert color, use `_set_pixel_and_convert_color()`.
        """
        if not self.is_in_bounds(x, y):
            return
        rgb = self._convert_rrggbb_to_image_color(color)
        x -= self._min_x
        y -= self._min_y
        self._image.putpixel((x, y), rgb)