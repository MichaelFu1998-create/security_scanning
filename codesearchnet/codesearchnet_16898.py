def flip(self, angle, center=None):
        """ Flip the shape in an arbitrary direction.

        Parameters
        ----------
        angle : array-like
            The angle, in radians counter-clockwise from the horizontal axis,
            defining the angle about which to flip the shape (of a line through `center`).
        center : array-like, optional
            The point about which to flip.
            If not passed, the center of the shape will be used.

        """
        return self.rotate(-angle, center=center).flip_y(center=center).rotate(angle, center=center)