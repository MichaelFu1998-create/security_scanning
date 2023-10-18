def set(self, point):
        """Set pixel at (x, y) point."""
        if not isinstance(point, Point):
            point = Point(point)

        rx = self.round(point.x)
        ry = self.round(point.y)

        item = Point((rx >> 1, min(ry >> 2, self.size.y)))
        self.screen[item] |= self.pixels[ry & 3][rx & 1]