def compute_pointwise_distances(self, other, default=None):
        """
        Compute the minimal distance between each point on self and other.

        Parameters
        ----------
        other : tuple of number \
                or imgaug.augmentables.kps.Keypoint \
                or imgaug.augmentables.LineString
            Other object to which to compute the distances.

        default
            Value to return if `other` contains no points.

        Returns
        -------
        list of float
            Distances to `other` or `default` if not distance could be computed.

        """
        import shapely.geometry
        from .kps import Keypoint

        if isinstance(other, Keypoint):
            other = shapely.geometry.Point((other.x, other.y))
        elif isinstance(other, LineString):
            if len(other.coords) == 0:
                return default
            elif len(other.coords) == 1:
                other = shapely.geometry.Point(other.coords[0, :])
            else:
                other = shapely.geometry.LineString(other.coords)
        elif isinstance(other, tuple):
            assert len(other) == 2
            other = shapely.geometry.Point(other)
        else:
            raise ValueError(
                ("Expected Keypoint or LineString or tuple (x,y), "
                 + "got type %s.") % (type(other),))

        return [shapely.geometry.Point(point).distance(other)
                for point in self.coords]