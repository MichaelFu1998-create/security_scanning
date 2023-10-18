def update(self, points, values=None):
        """Add a set of data points."""
        self.values = values or [None] * len(points)

        if np is None:
            if self.option.function:
                warnings.warn('numpy not available, function ignored')
            self.points = points
            self.minimum = min(self.points)
            self.maximum = max(self.points)
            self.current = self.points[-1]

        else:
            self.points = self.apply_function(points)
            self.minimum = np.min(self.points)
            self.maximum = np.max(self.points)
            self.current = self.points[-1]

        if self.maximum == self.minimum:
            self.extents = 1
        else:
            self.extents = (self.maximum - self.minimum)
            self.extents = (self.maximum - self.minimum)