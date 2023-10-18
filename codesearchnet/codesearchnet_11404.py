def unset(self, point):
        """Unset pixel at (x, y) point."""
        if not isinstance(point, Point):
            point = Point(point)

        x, y = self.round(point.x) >> 1, self.round(point.y) >> 2

        if (x, y) not in self.screen:
            return

        if isinstance(self.screen[y][x], int):
            self.screen[(x, y)] &= ~self.pixels[y & 3][x & 1]

        else:
            del self.screen[(x, y)]

        if not self.screen.canvas.get(y):
            del self.screen[y]