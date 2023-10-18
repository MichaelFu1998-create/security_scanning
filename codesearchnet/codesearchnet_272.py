def compute_distance(self, other, default=None):
        """
        Compute the minimal distance between the line string and `other`.

        Parameters
        ----------
        other : tuple of number \
                or imgaug.augmentables.kps.Keypoint \
                or imgaug.augmentables.LineString
            Other object to which to compute the distance.

        default
            Value to return if this line string or `other` contain no points.

        Returns
        -------
        float
            Distance to `other` or `default` if not distance could be computed.

        """
        # FIXME this computes distance pointwise, does not have to be identical
        #       with the actual min distance (e.g. edge center to other's point)
        distances = self.compute_pointwise_distances(other, default=[])
        if len(distances) == 0:
            return default
        return min(distances)