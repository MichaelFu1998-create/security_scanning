def projection_constants(self):
        """
        Returns the (x, y) projection constants for the current projection.
        :return: x, y tuple projection constants
        """
        return self.far / (self.far - self.near), (self.far * self.near) / (self.near - self.far)