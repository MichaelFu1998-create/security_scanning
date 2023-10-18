def almost_equals(self, other, max_distance=1e-6, points_per_edge=8):
        """
        Estimate if this polygon's and another's geometry/labels are similar.

        This is the same as :func:`imgaug.Polygon.exterior_almost_equals` but
        additionally compares the labels.

        Parameters
        ----------
        other
            The object to compare against. If not a Polygon, then False will
            be returned.

        max_distance : float, optional
            See :func:`imgaug.augmentables.polys.Polygon.exterior_almost_equals`.

        points_per_edge : int, optional
            See :func:`imgaug.augmentables.polys.Polygon.exterior_almost_equals`.

        Returns
        -------
        bool
            Whether the two polygons can be viewed as equal. In the case of
            the exteriors this is an approximate test.

        """
        if not isinstance(other, Polygon):
            return False
        if self.label is not None or other.label is not None:
            if self.label is None:
                return False
            if other.label is None:
                return False
            if self.label != other.label:
                return False
        return self.exterior_almost_equals(
            other, max_distance=max_distance, points_per_edge=points_per_edge)