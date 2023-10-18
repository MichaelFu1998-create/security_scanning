def sub_array_2d_from_sub_array_1d(self, sub_array_1d):
        """ Map a 1D sub-array the same dimension as the sub-grid (e.g. including sub-pixels) to its original masked
        2D sub array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub_array which is mapped to its masked 2D sub-array.
        """
        sub_shape = (self.mask.shape[0] * self.sub_grid_size, self.mask.shape[1] * self.sub_grid_size)
        sub_one_to_two = self.mask.masked_sub_grid_index_to_sub_pixel(sub_grid_size=self.sub_grid_size)
        return mapping_util.map_masked_1d_array_to_2d_array_from_array_1d_shape_and_one_to_two(
            array_1d=sub_array_1d, shape=sub_shape, one_to_two=sub_one_to_two)