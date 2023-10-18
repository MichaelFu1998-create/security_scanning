def exterior_almost_equals(self, other, max_distance=1e-6, points_per_edge=8):
        """
        Estimate if this and other polygon's exterior are almost identical.

        The two exteriors can have different numbers of points, but any point
        randomly sampled on the exterior of one polygon should be close to the
        closest point on the exterior of the other polygon.

        Note that this method works approximately. One can come up with
        polygons with fairly different shapes that will still be estimated as
        equal by this method. In practice however this should be unlikely to be
        the case. The probability for something like that goes down as the
        interpolation parameter is increased.

        Parameters
        ----------
        other : imgaug.Polygon or (N,2) ndarray or list of tuple
            The other polygon with which to compare the exterior.
            If this is an ndarray, it is assumed to represent an exterior.
            It must then have dtype ``float32`` and shape ``(N,2)`` with the
            second dimension denoting xy-coordinates.
            If this is a list of tuples, it is assumed to represent an exterior.
            Each tuple then must contain exactly two numbers, denoting
            xy-coordinates.

        max_distance : number, optional
            The maximum euclidean distance between a point on one polygon and
            the closest point on the other polygon. If the distance is exceeded
            for any such pair, the two exteriors are not viewed as equal. The
            points are other the points contained in the polygon's exterior
            ndarray or interpolated points between these.

        points_per_edge : int, optional
            How many points to interpolate on each edge.

        Returns
        -------
        bool
            Whether the two polygon's exteriors can be viewed as equal
            (approximate test).

        """
        if isinstance(other, list):
            other = Polygon(np.float32(other))
        elif ia.is_np_array(other):
            other = Polygon(other)
        else:
            assert isinstance(other, Polygon)
            other = other

        return self.to_line_string(closed=True).coords_almost_equals(
            other.to_line_string(closed=True),
            max_distance=max_distance,
            points_per_edge=points_per_edge
        )