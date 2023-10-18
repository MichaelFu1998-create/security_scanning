def height(self):
        """Get the height of a bounding box encapsulating the line."""
        if len(self.coords) <= 1:
            return 0
        return np.max(self.yy) - np.min(self.yy)