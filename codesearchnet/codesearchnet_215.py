def change_first_point_by_index(self, point_idx):
        """
        Set the first point of the exterior to the given point based on its index.

        Note: This method does *not* work in-place.

        Parameters
        ----------
        point_idx : int
            Index of the desired starting point.

        Returns
        -------
        imgaug.Polygon
            Copy of this polygon with the new point order.

        """
        ia.do_assert(0 <= point_idx < len(self.exterior))
        if point_idx == 0:
            return self.deepcopy()
        exterior = np.concatenate(
            (self.exterior[point_idx:, :], self.exterior[:point_idx, :]),
            axis=0
        )
        return self.deepcopy(exterior=exterior)