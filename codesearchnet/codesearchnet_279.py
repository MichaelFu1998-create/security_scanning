def find_intersections_with(self, other):
        """
        Find all intersection points between the line string and `other`.

        Parameters
        ----------
        other : tuple of number or list of tuple of number or \
                list of LineString or LineString
            The other geometry to use during intersection tests.

        Returns
        -------
        list of list of tuple of number
            All intersection points. One list per pair of consecutive start
            and end point, i.e. `N-1` lists of `N` points. Each list may
            be empty or may contain multiple points.

        """
        import shapely.geometry

        geom = _convert_var_to_shapely_geometry(other)

        result = []
        for p_start, p_end in zip(self.coords[:-1], self.coords[1:]):
            ls = shapely.geometry.LineString([p_start, p_end])
            intersections = ls.intersection(geom)
            intersections = list(_flatten_shapely_collection(intersections))

            intersections_points = []
            for inter in intersections:
                if isinstance(inter, shapely.geometry.linestring.LineString):
                    inter_start = (inter.coords[0][0], inter.coords[0][1])
                    inter_end = (inter.coords[-1][0], inter.coords[-1][1])
                    intersections_points.extend([inter_start, inter_end])
                else:
                    assert isinstance(inter, shapely.geometry.point.Point), (
                        "Expected to find shapely.geometry.point.Point or "
                        "shapely.geometry.linestring.LineString intersection, "
                        "actually found %s." % (type(inter),))
                    intersections_points.append((inter.x, inter.y))

            # sort by distance to start point, this makes it later on easier
            # to remove duplicate points
            inter_sorted = sorted(
                intersections_points,
                key=lambda p: np.linalg.norm(np.float32(p) - p_start)
            )

            result.append(inter_sorted)
        return result