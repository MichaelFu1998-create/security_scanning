def width(self):
        """Get the width of a bounding box encapsulating the line."""
        if len(self.coords) <= 1:
            return 0
        return np.max(self.xx) - np.min(self.xx)