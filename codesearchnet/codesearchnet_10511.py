def load_poisson_noise_map(poisson_noise_map_path, poisson_noise_map_hdu, pixel_scale,
                           convert_poisson_noise_map_from_weight_map,
                           convert_poisson_noise_map_from_inverse_noise_map,
                           poisson_noise_map_from_image,
                           image, exposure_time_map, convert_from_electrons, gain, convert_from_adus):
    """Factory for loading the Poisson noise-map from a .fits file.

    This factory also includes a number of routines for converting the Poisson noise-map from from other units (e.g. \
    a weight map) or computing the Poisson noise_map from other unblurred_image_1d (e.g. the ccd image).

    Parameters
    ----------
    poisson_noise_map_path : str
        The path to the poisson_noise_map .fits file containing the Poisson noise-map \
         (e.g. '/path/to/poisson_noise_map.fits')
    poisson_noise_map_hdu : int
        The hdu the poisson_noise_map is contained in the .fits file specified by *poisson_noise_map_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    convert_poisson_noise_map_from_weight_map : bool
        If True, the Poisson noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_poisson_noise_map_from_inverse_noise_map : bool
        If True, the Poisson noise-map loaded from the .fits file is converted from an inverse noise-map to a \
        noise-map (see *NoiseMap.from_inverse_noise_map).
    poisson_noise_map_from_image : bool
        If True, the Poisson noise-map is estimated using the image.
    image : ndarray
        The image, which the Poisson noise-map can be calculated using.
    background_noise_map : ndarray
        The background noise-map, which the Poisson noise-map can be calculated using.
    exposure_time_map : ndarray
        The exposure-time map, which the Poisson noise-map can be calculated using.
    convert_from_electrons : bool
        If True, the input unblurred_image_1d are in units of electrons and all converted to electrons / second using the exposure \
        time map.
    gain : float
        The image gain, used for convert from ADUs.
    convert_from_adus : bool
        If True, the input unblurred_image_1d are in units of adus and all converted to electrons / second using the exposure \
        time map and gain.
    """
    poisson_noise_map_options = sum([convert_poisson_noise_map_from_weight_map,
                                     convert_poisson_noise_map_from_inverse_noise_map,
                                     poisson_noise_map_from_image])

    if poisson_noise_map_options == 0 and poisson_noise_map_path is not None:
        return PoissonNoiseMap.from_fits_with_pixel_scale(file_path=poisson_noise_map_path, hdu=poisson_noise_map_hdu,
                                                          pixel_scale=pixel_scale)
    elif poisson_noise_map_from_image:

        if not (convert_from_electrons or convert_from_adus) and exposure_time_map is None:
            raise exc.DataException('Cannot compute the Poisson noise-map from the image if an '
                                       'exposure-time (or exposure time map) is not supplied to convert to adus')

        if convert_from_adus and gain is None:
            raise exc.DataException('Cannot compute the Poisson noise-map from the image if a'
                                       'gain is not supplied to convert from adus')

        return PoissonNoiseMap.from_image_and_exposure_time_map(pixel_scale=pixel_scale, image=image,
                                                                exposure_time_map=exposure_time_map,
                                                                convert_from_electrons=convert_from_electrons,
                                                                gain=gain,
                                                                convert_from_adus=convert_from_adus)

    elif convert_poisson_noise_map_from_weight_map and poisson_noise_map_path is not None:
        weight_map = Array.from_fits(file_path=poisson_noise_map_path, hdu=poisson_noise_map_hdu)
        return PoissonNoiseMap.from_weight_map(weight_map=weight_map, pixel_scale=pixel_scale)
    elif convert_poisson_noise_map_from_inverse_noise_map and poisson_noise_map_path is not None:
        inverse_noise_map = Array.from_fits(file_path=poisson_noise_map_path, hdu=poisson_noise_map_hdu)
        return PoissonNoiseMap.from_inverse_noise_map(inverse_noise_map=inverse_noise_map, pixel_scale=pixel_scale)
    else:
        return None