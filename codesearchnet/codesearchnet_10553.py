def convolve_array_1d_with_psf(self, padded_array_1d, psf):
        """Convolve a 1d padded array of values (e.g. intensities before PSF blurring) with a PSF, and then trim \
        the convolved array to its original 2D shape.

        Parameters
        -----------
        padded_array_1d: ndarray
            A 1D array of values which were computed using the *PaddedRegularGrid*.
        psf : ndarray
            An array describing the PSF kernel of the image.
        """
        padded_array_2d = mapping_util.map_unmasked_1d_array_to_2d_array_from_array_1d_and_shape(
            array_1d=padded_array_1d, shape=self.mask.shape)
        # noinspection PyUnresolvedReferences
        blurred_padded_array_2d = psf.convolve(array=padded_array_2d)
        return mapping_util.map_2d_array_to_masked_1d_array_from_array_2d_and_mask(array_2d=blurred_padded_array_2d,
                                                                                   mask=np.full(self.mask.shape, False))