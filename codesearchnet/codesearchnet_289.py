def concatenate(self, other):
        """
        Concatenate this line string with another one.

        This will add a line segment between the end point of this line string
        and the start point of `other`.

        Parameters
        ----------
        other : imgaug.augmentables.lines.LineString or ndarray \
                or iterable of tuple of number
            The points to add to this line string.

        Returns
        -------
        imgaug.augmentables.lines.LineString
            New line string with concatenated points.
            The `label` of this line string will be kept.

        """
        if not isinstance(other, LineString):
            other = LineString(other)
        return self.deepcopy(
            coords=np.concatenate([self.coords, other.coords], axis=0))