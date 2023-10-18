def compute_neighbour_distances(self):
        """
        Get the euclidean distance between each two consecutive points.

        Returns
        -------
        ndarray
            Euclidean distances between point pairs.
            Same order as in `coords`. For ``N`` points, ``N-1`` distances
            are returned.

        """
        if len(self.coords) <= 1:
            return np.zeros((0,), dtype=np.float32)
        return np.sqrt(
            np.sum(
                (self.coords[:-1, :] - self.coords[1:, :]) ** 2,
                axis=1
            )
        )