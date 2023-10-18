def get(self, x, y):
        """
        Return the pixel color at position (x, y), or Colors.black if that
        position is out-of-bounds.
        """
        try:
            pixel = self.coord_map[y][x]
            return self._get_base(pixel)
        except IndexError:
            return colors.COLORS.Black