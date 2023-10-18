def load_exposure_time_map(exposure_time_map_path, exposure_time_map_hdu, pixel_scale, shape, exposure_time,
                           exposure_time_map_from_inverse_noise_map, inverse_noise_map):
    """Factory for loading the exposure time map from a .fits file.

    This factory also includes a number of routines for computing the exposure-time map from other unblurred_image_1d \
    (e.g. the background noise-map).

    Parameters
    ----------
    exposure_time_map_path : str
        The path to the exposure_time_map .fits file containing the exposure time map \
        (e.g. '/path/to/exposure_time_map.fits')
    exposure_time_map_hdu : int
        The hdu the exposure_time_map is contained in the .fits file specified by *exposure_time_map_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    shape : (int, int)
        The shape of the image, required if a single value is used to calculate the exposure time map.
    exposure_time : float
        The exposure-time used to compute the expsure-time map if only a single value is used.
    exposure_time_map_from_inverse_noise_map : bool
        If True, the exposure-time map is computed from the background noise_map map \
        (see *ExposureTimeMap.from_background_noise_map*)
    inverse_noise_map : ndarray
        The background noise-map, which the Poisson noise-map can be calculated using.
    """
    exposure_time_map_options = sum([exposure_time_map_from_inverse_noise_map])

    if exposure_time is not None and exposure_time_map_path is not None:
        raise exc.DataException(
            'You have supplied both a exposure_time_map_path to an exposure time map and an exposure time. Only'
            'one quantity should be supplied.')

    if exposure_time_map_options == 0:

        if exposure_time is not None and exposure_time_map_path is None:
            return ExposureTimeMap.single_value(value=exposure_time, pixel_scale=pixel_scale, shape=shape)
        elif exposure_time is None and exposure_time_map_path is not None:
            return ExposureTimeMap.from_fits_with_pixel_scale(file_path=exposure_time_map_path,
                                                              hdu=exposure_time_map_hdu, pixel_scale=pixel_scale)

    else:

        if exposure_time_map_from_inverse_noise_map:
            return ExposureTimeMap.from_exposure_time_and_inverse_noise_map(pixel_scale=pixel_scale,
                                                                            exposure_time=exposure_time,
                                                                            inverse_noise_map=inverse_noise_map)