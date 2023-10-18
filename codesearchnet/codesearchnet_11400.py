def _normalised_numpy(self):
        """Normalised data points using numpy."""
        dx = (self.screen.width / float(len(self.points)))
        oy = (self.screen.height)
        points = np.array(self.points) - self.minimum
        points = points * 4.0 / self.extents * self.size.y
        for x, y in enumerate(points):
            yield Point((
                dx * x,
                min(oy, oy - y),
            ))