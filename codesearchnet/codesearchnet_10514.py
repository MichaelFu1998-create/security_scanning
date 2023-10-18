def load_background_sky_map(background_sky_map_path, background_sky_map_hdu, pixel_scale):
    """Factory for loading the background sky from a .fits file.

    Parameters
    ----------
    background_sky_map_path : str
        The path to the background_sky_map .fits file containing the background sky map \
        (e.g. '/path/to/background_sky_map.fits').
    background_sky_map_hdu : int
        The hdu the background_sky_map is contained in the .fits file specified by *background_sky_map_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    """
    if background_sky_map_path is not None:
        return ScaledSquarePixelArray.from_fits_with_pixel_scale(file_path=background_sky_map_path,
                                                                 hdu=background_sky_map_hdu, pixel_scale=pixel_scale)
    else:
        return None