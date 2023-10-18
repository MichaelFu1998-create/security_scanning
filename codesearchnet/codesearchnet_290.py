def subdivide(self, points_per_edge):
        """
        Adds ``N`` interpolated points with uniform spacing to each edge.

        For each edge between points ``A`` and ``B`` this adds points
        at ``A + (i/(1+N)) * (B - A)``, where ``i`` is the index of the added
        point and ``N`` is the number of points to add per edge.

        Calling this method two times will split each edge at its center
        and then again split each newly created edge at their center.
        It is equivalent to calling `subdivide(3)`.

        Parameters
        ----------
        points_per_edge : int
            Number of points to interpolate on each edge.

        Returns
        -------
        LineString
            Line string with subdivided edges.

        """
        if len(self.coords) <= 1 or points_per_edge < 1:
            return self.deepcopy()
        coords = interpolate_points(self.coords, nb_steps=points_per_edge,
                                    closed=False)
        return self.deepcopy(coords=coords)