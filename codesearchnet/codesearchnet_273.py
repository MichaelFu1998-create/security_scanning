def contains(self, other, max_distance=1e-4):
        """
        Estimate whether the bounding box contains a point.

        Parameters
        ----------
        other : tuple of number or imgaug.augmentables.kps.Keypoint
            Point to check for.

        max_distance : float
            Maximum allowed euclidean distance between the point and the
            closest point on the line. If the threshold is exceeded, the point
            is not considered to be contained in the line.

        Returns
        -------
        bool
            True if the point is contained in the line string, False otherwise.
            It is contained if its distance to the line or any of its points
            is below a threshold.

        """
        return self.compute_distance(other, default=np.inf) < max_distance