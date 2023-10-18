def find_closest_point_index(self, x, y, return_distance=False):
        """
        Find the index of the point within the exterior that is closest to the given coordinates.

        "Closeness" is here defined based on euclidean distance.
        This method will raise an AssertionError if the exterior contains no points.

        Parameters
        ----------
        x : number
            X-coordinate around which to search for close points.

        y : number
            Y-coordinate around which to search for close points.

        return_distance : bool, optional
            Whether to also return the distance of the closest point.

        Returns
        -------
        int
            Index of the closest point.

        number
            Euclidean distance to the closest point.
            This value is only returned if `return_distance` was set to True.

        """
        ia.do_assert(len(self.exterior) > 0)
        distances = []
        for x2, y2 in self.exterior:
            d = (x2 - x) ** 2 + (y2 - y) ** 2
            distances.append(d)
        distances = np.sqrt(distances)
        closest_idx = np.argmin(distances)
        if return_distance:
            return closest_idx, distances[closest_idx]
        return closest_idx