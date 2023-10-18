def almost_equals(self, other, max_distance=1e-4, points_per_edge=8):
        """
        Compare this and another LineString.

        Parameters
        ----------
        other: imgaug.augmentables.lines.LineString
            The other line string. Must be a LineString instance, not just
            its coordinates.

        max_distance : float, optional
            See :func:`imgaug.augmentables.lines.LineString.coords_almost_equals`.

        points_per_edge : int, optional
            See :func:`imgaug.augmentables.lines.LineString.coords_almost_equals`.

        Returns
        -------
        bool
            ``True`` if the coordinates are almost equal according to
            :func:`imgaug.augmentables.lines.LineString.coords_almost_equals`
            and additionally the labels are identical. Otherwise ``False``.

        """
        if self.label != other.label:
            return False
        return self.coords_almost_equals(
            other, max_distance=max_distance, points_per_edge=points_per_edge)