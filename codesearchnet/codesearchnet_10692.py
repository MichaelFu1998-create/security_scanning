def unmasked_blurred_image_of_galaxies_from_psf(self, padded_grid_stack, psf):
        """This is a utility function for the function above, which performs the iteration over each plane's galaxies \
        and computes each galaxy's unmasked blurred image.

        Parameters
        ----------
        padded_grid_stack
        psf : ccd.PSF
            The PSF of the image used for convolution.
        """
        return [padded_grid_stack.unmasked_blurred_image_from_psf_and_unmasked_image(
            psf, image) if not galaxy.has_pixelization else None for galaxy, image in
                zip(self.galaxies, self.image_plane_image_1d_of_galaxies)]