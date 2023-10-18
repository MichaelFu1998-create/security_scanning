def scaled_array_2d_with_sub_dimensions_from_sub_array_1d(self, sub_array_1d):
        """ Map a 1D sub-array the same dimension as the sub-grid to its original masked 2D sub-array and return it as
        a scaled array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub-array of which is mapped to a 2D scaled sub-array the dimensions.
        """
        return scaled_array.ScaledSquarePixelArray(array=self.sub_array_2d_from_sub_array_1d(sub_array_1d=sub_array_1d),
                                                   pixel_scale=self.mask.pixel_scale / self.sub_grid_size,
                                                   origin=self.mask.origin)