def null(self):
        """Zero crossing value."""
        if not self.option.axis:
            return -1
        else:
            return self.screen.height - (
                -self.minimum * 4.0 / self.extents * self.size.y
            )