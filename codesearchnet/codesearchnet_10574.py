def map_to_2d_keep_padded(self, padded_array_1d):
        """ Map a padded 1D array of values to its padded 2D array.

        Parameters
        -----------
        padded_array_1d : ndarray
            A 1D array of values which were computed using the *PaddedRegularGrid*.
        """
        return mapping_util.map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(array_1d=padded_array_1d,
                                                                                      shape=self.mask.shape)