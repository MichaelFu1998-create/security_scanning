def padded_blurred_image_2d_from_padded_image_1d_and_psf(self, padded_image_1d, psf):
        """Compute a 2D padded blurred image from a 1D padded image.

        Parameters
        ----------
        padded_image_1d : ndarray
            A 1D unmasked image which is blurred with the PSF.
        psf : ndarray
            An array describing the PSF kernel of the image.
        """
        padded_model_image_1d = self.convolve_array_1d_with_psf(padded_array_1d=padded_image_1d, psf=psf)
        return self.scaled_array_2d_from_array_1d(array_1d=padded_model_image_1d)