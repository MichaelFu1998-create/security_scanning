def flip_y(self, center=None):
        """Flip the shape in the y direction, in-place.

        Parameters
        ----------
        center : array-like, optional
            Point about which to flip.
            If not passed, the center of the shape will be used.

         """
        if center is None:
            self.poly.flop()
        else:
            self.poly.flop(center[1])
        return self