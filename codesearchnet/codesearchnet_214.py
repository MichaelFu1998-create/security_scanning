def change_first_point_by_coords(self, x, y, max_distance=1e-4,
                                     raise_if_too_far_away=True):
        """
        Set the first point of the exterior to the given point based on its coordinates.

        If multiple points are found, the closest one will be picked.
        If no matching points are found, an exception is raised.

        Note: This method does *not* work in-place.

        Parameters
        ----------
        x : number
            X-coordinate of the point.

        y : number
            Y-coordinate of the point.

        max_distance : None or number, optional
            Maximum distance past which possible matches are ignored.
            If ``None`` the distance limit is deactivated.

        raise_if_too_far_away : bool, optional
            Whether to raise an exception if the closest found point is too
            far away (``True``) or simply return an unchanged copy if this
            object (``False``).

        Returns
        -------
        imgaug.Polygon
            Copy of this polygon with the new point order.

        """
        if len(self.exterior) == 0:
            raise Exception("Cannot reorder polygon points, because it contains no points.")

        closest_idx, closest_dist = self.find_closest_point_index(x=x, y=y, return_distance=True)
        if max_distance is not None and closest_dist > max_distance:
            if not raise_if_too_far_away:
                return self.deepcopy()

            closest_point = self.exterior[closest_idx, :]
            raise Exception(
                "Closest found point (%.9f, %.9f) exceeds max_distance of %.9f exceeded" % (
                    closest_point[0], closest_point[1], closest_dist)
            )
        return self.change_first_point_by_index(closest_idx)