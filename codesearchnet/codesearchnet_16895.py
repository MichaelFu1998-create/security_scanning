def rotate(self, angle, center=None):
        """Rotate the shape, in-place.

        Parameters
        ----------
        angle : float
            Angle to rotate, in radians counter-clockwise.
        center : array-like, optional
            Point about which to rotate.
            If not passed, the center of the shape will be used.

        """
        args = [angle]
        if center is not None:
            args.extend(center)
        self.poly.rotate(*args)
        return self