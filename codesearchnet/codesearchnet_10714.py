def map_2d_array_to_masked_1d_array(self, array_2d):
        """For a 2D array (e.g. an image, noise_map, etc.) map it to a masked 1D array of valuees using this mask.

        Parameters
        ----------
        array_2d : ndarray | None | float
            The 2D array to be mapped to a masked 1D array.
        """
        if array_2d is None or isinstance(array_2d, float):
            return array_2d
        return mapping_util.map_2d_array_to_masked_1d_array_from_array_2d_and_mask(self, array_2d)