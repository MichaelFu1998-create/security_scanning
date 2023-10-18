def convolve_image(self, image_array, blurring_array):
        """For a given 1D regular array and blurring array, convolve the two using this convolver.

        Parameters
        -----------
        image_array : ndarray
            1D array of the regular values which are to be blurred with the convolver's PSF.
        blurring_array : ndarray
            1D array of the blurring regular values which blur into the regular-array after PSF convolution.
        """
        return self.convolve_jit(image_array, self.image_frame_indexes, self.image_frame_psfs, self.image_frame_lengths,
                                 blurring_array, self.blurring_frame_indexes, self.blurring_frame_psfs,
                                 self.blurring_frame_lengths)