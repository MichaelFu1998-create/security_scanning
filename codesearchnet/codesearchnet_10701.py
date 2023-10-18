def from_fits_with_pixel_scale(cls, file_path, hdu, pixel_scale, origin=(0.0, 0.0)):
        """
        Loads the image from a .fits file.

        Parameters
        ----------
        file_path : str
            The full path of the fits file.
        hdu : int
            The HDU number in the fits file containing the image image.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        return cls(array_util.numpy_array_2d_from_fits(file_path, hdu), pixel_scale, origin)