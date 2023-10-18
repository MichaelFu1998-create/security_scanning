def new_psf_with_renormalized_array(self):
        """Renormalize the PSF such that its data_vector values sum to unity."""
        return PSF(array=self, pixel_scale=self.pixel_scale, renormalize=True)