def scaled_array_2d_from_array_1d(self, array_1d):
        """ Map a 1D array the same dimension as the grid to its original masked 2D array and return it as a scaled \
        array.

        Parameters
        -----------
        array_1d : ndarray
            The 1D array of which is mapped to a 2D scaled array.
        """
        return scaled_array.ScaledSquarePixelArray(array=self.array_2d_from_array_1d(array_1d),
                                                   pixel_scale=self.mask.pixel_scale,
                                                   origin=self.mask.origin)