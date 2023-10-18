def array_2d_from_array_1d(self, padded_array_1d):
        """ Map a padded 1D array of values to its original 2D array, trimming all edge values.

        Parameters
        -----------
        padded_array_1d : ndarray
            A 1D array of values which were computed using the *PaddedRegularGrid*.
        """
        padded_array_2d = self.map_to_2d_keep_padded(padded_array_1d)
        pad_size_0 = self.mask.shape[0] - self.image_shape[0]
        pad_size_1 = self.mask.shape[1] - self.image_shape[1]
        return (padded_array_2d[pad_size_0 // 2:self.mask.shape[0] - pad_size_0 // 2,
                pad_size_1 // 2:self.mask.shape[1] - pad_size_1 // 2])