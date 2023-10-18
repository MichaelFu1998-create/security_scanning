def load_background_noise_map(background_noise_map_path, background_noise_map_hdu, pixel_scale,
                              convert_background_noise_map_from_weight_map,
                              convert_background_noise_map_from_inverse_noise_map):
    """Factory for loading the background noise-map from a .fits file.

    This factory also includes a number of routines for converting the background noise-map from from other units (e.g. \
    a weight map).

    Parameters
    ----------
    background_noise_map_path : str
        The path to the background_noise_map .fits file containing the background noise-map \
        (e.g. '/path/to/background_noise_map.fits')
    background_noise_map_hdu : int
        The hdu the background_noise_map is contained in the .fits file specified by *background_noise_map_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    convert_background_noise_map_from_weight_map : bool
        If True, the bacground noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_background_noise_map_from_inverse_noise_map : bool
        If True, the background noise-map loaded from the .fits file is converted from an inverse noise-map to a \
        noise-map (see *NoiseMap.from_inverse_noise_map).
    """
    background_noise_map_options = sum([convert_background_noise_map_from_weight_map,
                                        convert_background_noise_map_from_inverse_noise_map])

    if background_noise_map_options == 0 and background_noise_map_path is not None:
        return NoiseMap.from_fits_with_pixel_scale(file_path=background_noise_map_path, hdu=background_noise_map_hdu,
                                                   pixel_scale=pixel_scale)
    elif convert_background_noise_map_from_weight_map and background_noise_map_path is not None:
        weight_map = Array.from_fits(file_path=background_noise_map_path, hdu=background_noise_map_hdu)
        return NoiseMap.from_weight_map(weight_map=weight_map, pixel_scale=pixel_scale)
    elif convert_background_noise_map_from_inverse_noise_map and background_noise_map_path is not None:
        inverse_noise_map = Array.from_fits(file_path=background_noise_map_path, hdu=background_noise_map_hdu)
        return NoiseMap.from_inverse_noise_map(inverse_noise_map=inverse_noise_map, pixel_scale=pixel_scale)
    else:
        return None