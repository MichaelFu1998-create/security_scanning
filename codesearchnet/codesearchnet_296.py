def coords_almost_equals(self, other, max_distance=1e-6, points_per_edge=8):
        """
        Compare this and another LineString's coordinates.

        This is an approximate method based on pointwise distances and can
        in rare corner cases produce wrong outputs.

        Parameters
        ----------
        other : imgaug.augmentables.lines.LineString \
                or tuple of number \
                or ndarray \
                or list of ndarray \
                or list of tuple of number
            The other line string or its coordinates.

        max_distance : float
            Max distance of any point from the other line string before
            the two line strings are evaluated to be unequal.

        points_per_edge : int, optional
            How many points to interpolate on each edge.

        Returns
        -------
        bool
            Whether the two LineString's coordinates are almost identical,
            i.e. the max distance is below the threshold.
            If both have no coordinates, ``True`` is returned.
            If only one has no coordinates, ``False`` is returned.
            Beyond that, the number of points is not evaluated.

        """
        if isinstance(other, LineString):
            pass
        elif isinstance(other, tuple):
            other = LineString([other])
        else:
            other = LineString(other)

        if len(self.coords) == 0 and len(other.coords) == 0:
            return True
        elif 0 in [len(self.coords), len(other.coords)]:
            # only one of the two line strings has no coords
            return False

        self_subd = self.subdivide(points_per_edge)
        other_subd = other.subdivide(points_per_edge)

        dist_self2other = self_subd.compute_pointwise_distances(other_subd)
        dist_other2self = other_subd.compute_pointwise_distances(self_subd)
        dist = max(np.max(dist_self2other), np.max(dist_other2self))
        return  dist < max_distance