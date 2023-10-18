def flip_x(self, center=None):
        """Flip the shape in the x direction, in-place.

        Parameters
        ----------
        center : array-like, optional
            Point about which to flip.
            If not passed, the center of the shape will be used.

         """
        if center is None:
            self.poly.flip()
        else:
            self.poly.flip(center[0])