def load_noise_map(noise_map_path, noise_map_hdu, pixel_scale, image, background_noise_map, exposure_time_map,
                   convert_noise_map_from_weight_map, convert_noise_map_from_inverse_noise_map,
                   noise_map_from_image_and_background_noise_map, convert_from_electrons, gain, convert_from_adus):
    """Factory for loading the noise-map from a .fits file.

    This factory also includes a number of routines for converting the noise-map from from other units (e.g. \
    a weight map) or computing the noise-map from other unblurred_image_1d (e.g. the ccd image and background noise-map).

    Parameters
    ----------
    noise_map_path : str
        The path to the noise_map .fits file containing the noise_map (e.g. '/path/to/noise_map.fits')
    noise_map_hdu : int
        The hdu the noise_map is contained in the .fits file specified by *noise_map_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    image : ndarray
        The image-image, which the noise-map can be calculated using.
    background_noise_map : ndarray
        The background noise-map, which the noise-map can be calculated using.
    exposure_time_map : ndarray
        The exposure-time map, which the noise-map can be calculated using.
    convert_noise_map_from_weight_map : bool
        If True, the noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_noise_map_from_inverse_noise_map : bool
        If True, the noise-map loaded from the .fits file is converted from an inverse noise-map to a noise-map (see \
        *NoiseMap.from_inverse_noise_map).
    background_noise_map_path : str
        The path and filename of the .fits image containing the background noise-map.
    background_noise_map_hdu : int
        The hdu the background noise-map is contained in the .fits file that *background_noise_map_path* points too.
    convert_background_noise_map_from_weight_map : bool
        If True, the bacground noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_background_noise_map_from_inverse_noise_map : bool
        If True, the background noise-map loaded from the .fits file is converted from an inverse noise-map to a \
        noise-map (see *NoiseMap.from_inverse_noise_map).
    noise_map_from_image_and_background_noise_map : bool
        If True, the noise-map is computed from the observed image and background noise-map \
        (see NoiseMap.from_image_and_background_noise_map).
    convert_from_electrons : bool
        If True, the input unblurred_image_1d are in units of electrons and all converted to electrons / second using the exposure \
        time map.
    gain : float
        The image gain, used for convert from ADUs.
    convert_from_adus : bool
        If True, the input unblurred_image_1d are in units of adus and all converted to electrons / second using the exposure \
        time map and gain.
    """
    noise_map_options = sum([convert_noise_map_from_weight_map,
                             convert_noise_map_from_inverse_noise_map,
                             noise_map_from_image_and_background_noise_map])

    if noise_map_options > 1:
        raise exc.DataException('You have specified more than one method to load the noise_map map, e.g.:'
                                   'convert_noise_map_from_weight_map | '
                                   'convert_noise_map_from_inverse_noise_map |'
                                   'noise_map_from_image_and_background_noise_map')

    if noise_map_options == 0 and noise_map_path is not None:
        return NoiseMap.from_fits_with_pixel_scale(file_path=noise_map_path, hdu=noise_map_hdu, pixel_scale=pixel_scale)
    elif convert_noise_map_from_weight_map and noise_map_path is not None:
        weight_map = Array.from_fits(file_path=noise_map_path, hdu=noise_map_hdu)
        return NoiseMap.from_weight_map(weight_map=weight_map, pixel_scale=pixel_scale)
    elif convert_noise_map_from_inverse_noise_map and noise_map_path is not None:
        inverse_noise_map = Array.from_fits(file_path=noise_map_path, hdu=noise_map_hdu)
        return NoiseMap.from_inverse_noise_map(inverse_noise_map=inverse_noise_map, pixel_scale=pixel_scale)
    elif noise_map_from_image_and_background_noise_map:

        if background_noise_map is None:
            raise exc.DataException('Cannot compute the noise-map from the image and background noise_map map if a '
                                       'background noise_map map is not supplied.')

        if not (convert_from_electrons or convert_from_adus) and exposure_time_map is None:
            raise exc.DataException('Cannot compute the noise-map from the image and background noise_map map if an '
                                       'exposure-time (or exposure time map) is not supplied to convert to adus')

        if convert_from_adus and gain is None:
            raise exc.DataException('Cannot compute the noise-map from the image and background noise_map map if a'
                                       'gain is not supplied to convert from adus')

        return NoiseMap.from_image_and_background_noise_map(pixel_scale=pixel_scale, image=image,
                                                            background_noise_map=background_noise_map,
                                                            exposure_time_map=exposure_time_map,
                                                            convert_from_electrons=convert_from_electrons,
                                                            gain=gain, convert_from_adus=convert_from_adus)
    else:
        raise exc.DataException(
            'A noise_map map was not loaded, specify a noise_map_path or option to compute a noise_map map.')