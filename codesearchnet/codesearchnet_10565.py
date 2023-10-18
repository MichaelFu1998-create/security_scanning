def scaled_array_2d_with_regular_dimensions_from_binned_up_sub_array_1d(self, sub_array_1d):
        """ Map a 1D sub-array the same dimension as the sub-grid to its original masked 2D sub-array and return it as
        a scaled array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub-array of which is mapped to a 2D scaled sub-array the dimensions.
        """
        array_1d = self.regular_data_1d_from_sub_data_1d(sub_array_1d=sub_array_1d)
        return scaled_array.ScaledSquarePixelArray(array=self.array_2d_from_array_1d(array_1d=array_1d),
                                                   pixel_scale=self.mask.pixel_scale,
                                                   origin=self.mask.origin)