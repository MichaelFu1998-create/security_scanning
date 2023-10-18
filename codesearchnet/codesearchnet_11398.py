def set_text(self, point, text):
        """Set a text value in the screen canvas."""
        if not self.option.legend:
            return

        if not isinstance(point, Point):
            point = Point(point)

        for offset, char in enumerate(str(text)):
            self.screen.canvas[point.y][point.x + offset] = char