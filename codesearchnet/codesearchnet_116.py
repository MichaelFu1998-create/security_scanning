def contains(self, other):
        """
        Estimate whether the bounding box contains a point.

        Parameters
        ----------
        other : tuple of number or imgaug.Keypoint
            Point to check for.

        Returns
        -------
        bool
            True if the point is contained in the bounding box, False otherwise.

        """
        if isinstance(other, tuple):
            x, y = other
        else:
            x, y = other.x, other.y
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2