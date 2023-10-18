def from_fits_with_scale(cls, file_path, hdu, pixel_scale):
        """
        Loads the PSF from a .fits file.

        Parameters
        ----------
        pixel_scale
        file_path: String
            The path to the file containing the PSF
        hdu : int
            The HDU the PSF is stored in the .fits file.
        """
        return cls(array=array_util.numpy_array_2d_from_fits(file_path, hdu), pixel_scale=pixel_scale)