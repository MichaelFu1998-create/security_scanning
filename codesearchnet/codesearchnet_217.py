def to_shapely_line_string(self, closed=False, interpolate=0):
        """
        Convert this polygon to a Shapely LineString object.

        Parameters
        ----------
        closed : bool, optional
            Whether to return the line string with the last point being identical to the first point.

        interpolate : int, optional
            Number of points to interpolate between any pair of two consecutive points. These points are added
            to the final line string.

        Returns
        -------
        shapely.geometry.LineString
            The Shapely LineString matching the polygon's exterior.

        """
        return _convert_points_to_shapely_line_string(self.exterior, closed=closed, interpolate=interpolate)