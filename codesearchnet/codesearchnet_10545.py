def unmasked_blurred_image_from_psf_and_unmasked_image(self, psf, unmasked_image_1d):
        """For a padded grid-stack and psf, compute an unmasked blurred image from an unmasked unblurred image.

        This relies on using the lens data's padded-grid, which is a grid of (y,x) coordinates which extends over the \
        entire image as opposed to just the masked region.

        Parameters
        ----------
        psf : ccd.PSF
            The PSF of the image used for convolution.
        unmasked_image_1d : ndarray
            The 1D unmasked image which is blurred.
        """
        blurred_image_1d = self.regular.convolve_array_1d_with_psf(padded_array_1d=unmasked_image_1d,
                                                                   psf=psf)

        return self.regular.scaled_array_2d_from_array_1d(array_1d=blurred_image_1d)