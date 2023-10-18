def centers(self):
        """Returns the coordinates of the centers of all grid cells as an
        iterator."""
        for idx in numpy.ndindex(self.grid.shape):
            yield self.delta * numpy.array(idx) + self.origin