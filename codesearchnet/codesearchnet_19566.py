def rgb_color(self):
        """Return the color property as list of [R, G, B], each 0-255."""
        self.update()
        return [self._red, self._green, self._blue]