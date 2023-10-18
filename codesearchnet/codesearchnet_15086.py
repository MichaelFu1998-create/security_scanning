def _convert_to_image_color(self, color):
        """:return: a color that can be used by the image"""
        rgb = self._convert_color_to_rrggbb(color)
        return self._convert_rrggbb_to_image_color(rgb)