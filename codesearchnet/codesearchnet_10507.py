def load_ccd_data_from_fits(image_path, pixel_scale, image_hdu=0,
                            resized_ccd_shape=None, resized_ccd_origin_pixels=None,
                            resized_ccd_origin_arcsec=None,
                            psf_path=None, psf_hdu=0, resized_psf_shape=None, renormalize_psf=True,
                            noise_map_path=None, noise_map_hdu=0,
                            noise_map_from_image_and_background_noise_map=False,
                            convert_noise_map_from_weight_map=False,
                            convert_noise_map_from_inverse_noise_map=False,
                            background_noise_map_path=None, background_noise_map_hdu=0,
                            convert_background_noise_map_from_weight_map=False,
                            convert_background_noise_map_from_inverse_noise_map=False,
                            poisson_noise_map_path=None, poisson_noise_map_hdu=0,
                            poisson_noise_map_from_image=False,
                            convert_poisson_noise_map_from_weight_map=False,
                            convert_poisson_noise_map_from_inverse_noise_map=False,
                            exposure_time_map_path=None, exposure_time_map_hdu=0,
                            exposure_time_map_from_single_value=None,
                            exposure_time_map_from_inverse_noise_map=False,
                            background_sky_map_path=None, background_sky_map_hdu=0,
                            convert_from_electrons=False,
                            gain=None, convert_from_adus=False, lens_name=None):
    """Factory for loading the ccd data from .fits files, as well as computing properties like the noise-map,
    exposure-time map, etc. from the ccd-data.

    This factory also includes a number of routines for converting the ccd-data from units not supported by PyAutoLens \
    (e.g. adus, electrons) to electrons per second.

    Parameters
    ----------
    lens_name
    image_path : str
        The path to the image .fits file containing the image (e.g. '/path/to/image.fits')
    pixel_scale : float
        The size of each pixel in arc seconds.
    image_hdu : int
        The hdu the image is contained in the .fits file specified by *image_path*.        
    image_hdu : int
        The hdu the image is contained in the .fits file that *image_path* points too.
    resized_ccd_shape : (int, int) | None
        If input, the ccd arrays that are image sized, e.g. the image, noise-maps) are resized to these dimensions.
    resized_ccd_origin_pixels : (int, int) | None
        If the ccd arrays are resized, this defines a new origin (in pixels) around which recentering occurs.
    resized_ccd_origin_arcsec : (float, float) | None
        If the ccd arrays are resized, this defines a new origin (in arc-seconds) around which recentering occurs.
    psf_path : str
        The path to the psf .fits file containing the psf (e.g. '/path/to/psf.fits')        
    psf_hdu : int
        The hdu the psf is contained in the .fits file specified by *psf_path*.
    resized_psf_shape : (int, int) | None
        If input, the psf is resized to these dimensions.
    renormalize_psf : bool
        If True, the PSF is renoralized such that all elements sum to 1.0.
    noise_map_path : str
        The path to the noise_map .fits file containing the noise_map (e.g. '/path/to/noise_map.fits')        
    noise_map_hdu : int
        The hdu the noise_map is contained in the .fits file specified by *noise_map_path*.
    noise_map_from_image_and_background_noise_map : bool
        If True, the noise-map is computed from the observed image and background noise-map \
        (see NoiseMap.from_image_and_background_noise_map).
    convert_noise_map_from_weight_map : bool
        If True, the noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_noise_map_from_inverse_noise_map : bool
        If True, the noise-map loaded from the .fits file is converted from an inverse noise-map to a noise-map (see \
        *NoiseMap.from_inverse_noise_map).
    background_noise_map_path : str
        The path to the background_noise_map .fits file containing the background noise-map \ 
        (e.g. '/path/to/background_noise_map.fits')        
    background_noise_map_hdu : int
        The hdu the background_noise_map is contained in the .fits file specified by *background_noise_map_path*.
    convert_background_noise_map_from_weight_map : bool
        If True, the bacground noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_background_noise_map_from_inverse_noise_map : bool
        If True, the background noise-map loaded from the .fits file is converted from an inverse noise-map to a \
        noise-map (see *NoiseMap.from_inverse_noise_map).
    poisson_noise_map_path : str
        The path to the poisson_noise_map .fits file containing the Poisson noise-map \
         (e.g. '/path/to/poisson_noise_map.fits')        
    poisson_noise_map_hdu : int
        The hdu the poisson_noise_map is contained in the .fits file specified by *poisson_noise_map_path*.
    poisson_noise_map_from_image : bool
        If True, the Poisson noise-map is estimated using the image.
    convert_poisson_noise_map_from_weight_map : bool
        If True, the Poisson noise-map loaded from the .fits file is converted from a weight-map to a noise-map (see \
        *NoiseMap.from_weight_map).
    convert_poisson_noise_map_from_inverse_noise_map : bool
        If True, the Poisson noise-map loaded from the .fits file is converted from an inverse noise-map to a \
        noise-map (see *NoiseMap.from_inverse_noise_map).
    exposure_time_map_path : str
        The path to the exposure_time_map .fits file containing the exposure time map \ 
        (e.g. '/path/to/exposure_time_map.fits')        
    exposure_time_map_hdu : int
        The hdu the exposure_time_map is contained in the .fits file specified by *exposure_time_map_path*.
    exposure_time_map_from_single_value : float
        The exposure time of the ccd imaging, which is used to compute the exposure-time map as a single value \
        (see *ExposureTimeMap.from_single_value*).
    exposure_time_map_from_inverse_noise_map : bool
        If True, the exposure-time map is computed from the background noise_map map \
        (see *ExposureTimeMap.from_background_noise_map*)
    background_sky_map_path : str
        The path to the background_sky_map .fits file containing the background sky map \
        (e.g. '/path/to/background_sky_map.fits').
    background_sky_map_hdu : int
        The hdu the background_sky_map is contained in the .fits file specified by *background_sky_map_path*.
    convert_from_electrons : bool
        If True, the input unblurred_image_1d are in units of electrons and all converted to electrons / second using the exposure \
        time map.
    gain : float
        The image gain, used for convert from ADUs.
    convert_from_adus : bool
        If True, the input unblurred_image_1d are in units of adus and all converted to electrons / second using the exposure \
        time map and gain.
    """

    image = load_image(image_path=image_path, image_hdu=image_hdu, pixel_scale=pixel_scale)

    background_noise_map = load_background_noise_map(background_noise_map_path=background_noise_map_path,
                                                     background_noise_map_hdu=background_noise_map_hdu,
                                                     pixel_scale=pixel_scale,
                                                     convert_background_noise_map_from_weight_map=convert_background_noise_map_from_weight_map,
                                                     convert_background_noise_map_from_inverse_noise_map=convert_background_noise_map_from_inverse_noise_map)

    if background_noise_map is not None:
        inverse_noise_map = 1.0 / background_noise_map
    else:
        inverse_noise_map = None

    exposure_time_map = load_exposure_time_map(exposure_time_map_path=exposure_time_map_path,
                                               exposure_time_map_hdu=exposure_time_map_hdu,
                                               pixel_scale=pixel_scale, shape=image.shape,
                                               exposure_time=exposure_time_map_from_single_value,
                                               exposure_time_map_from_inverse_noise_map=exposure_time_map_from_inverse_noise_map,
                                               inverse_noise_map=inverse_noise_map)

    poisson_noise_map = load_poisson_noise_map(poisson_noise_map_path=poisson_noise_map_path,
                                               poisson_noise_map_hdu=poisson_noise_map_hdu,
                                               pixel_scale=pixel_scale,
                                               convert_poisson_noise_map_from_weight_map=convert_poisson_noise_map_from_weight_map,
                                               convert_poisson_noise_map_from_inverse_noise_map=convert_poisson_noise_map_from_inverse_noise_map,
                                               image=image, exposure_time_map=exposure_time_map,
                                               poisson_noise_map_from_image=poisson_noise_map_from_image,
                                               convert_from_electrons=convert_from_electrons, gain=gain,
                                               convert_from_adus=convert_from_adus)

    noise_map = load_noise_map(noise_map_path=noise_map_path, noise_map_hdu=noise_map_hdu, pixel_scale=pixel_scale,
                               image=image, background_noise_map=background_noise_map,
                               exposure_time_map=exposure_time_map,
                               convert_noise_map_from_weight_map=convert_noise_map_from_weight_map,
                               convert_noise_map_from_inverse_noise_map=convert_noise_map_from_inverse_noise_map,
                               noise_map_from_image_and_background_noise_map=noise_map_from_image_and_background_noise_map,
                               convert_from_electrons=convert_from_electrons, gain=gain,
                               convert_from_adus=convert_from_adus)

    psf = load_psf(psf_path=psf_path, psf_hdu=psf_hdu, pixel_scale=pixel_scale, renormalize=renormalize_psf)

    background_sky_map = load_background_sky_map(background_sky_map_path=background_sky_map_path,
                                                 background_sky_map_hdu=background_sky_map_hdu,
                                                 pixel_scale=pixel_scale)

    image = CCDData(image=image, pixel_scale=pixel_scale, psf=psf, noise_map=noise_map,
                    background_noise_map=background_noise_map, poisson_noise_map=poisson_noise_map,
                    exposure_time_map=exposure_time_map, background_sky_map=background_sky_map, gain=gain,
                    name=lens_name)

    if resized_ccd_shape is not None:
        image = image.new_ccd_data_with_resized_arrays(new_shape=resized_ccd_shape,
                                                       new_centre_pixels=resized_ccd_origin_pixels,
                                                       new_centre_arcsec=resized_ccd_origin_arcsec)

    if resized_psf_shape is not None:
        image = image.new_ccd_data_with_resized_psf(new_shape=resized_psf_shape)

    if convert_from_electrons:
        image = image.new_ccd_data_converted_from_electrons()
    elif convert_from_adus:
        image = image.new_ccd_data_converted_from_adus(gain=gain)

    return image