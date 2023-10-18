def _normalised_python(self):
        """Normalised data points using pure Python."""
        dx = (self.screen.width / float(len(self.points)))
        oy = (self.screen.height)
        for x, point in enumerate(self.points):
            y = (point - self.minimum) * 4.0 / self.extents * self.size.y
            yield Point((
                dx * x,
                min(oy, oy - y),
            ))