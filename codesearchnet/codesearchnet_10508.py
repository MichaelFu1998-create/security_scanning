def load_image(image_path, image_hdu, pixel_scale):
    """Factory for loading the image from a .fits file

    Parameters
    ----------
    image_path : str
        The path to the image .fits file containing the image (e.g. '/path/to/image.fits')
    image_hdu : int
        The hdu the image is contained in the .fits file specified by *image_path*.
    pixel_scale : float
        The size of each pixel in arc seconds..
    """
    return ScaledSquarePixelArray.from_fits_with_pixel_scale(file_path=image_path, hdu=image_hdu,
                                                             pixel_scale=pixel_scale)