def simulate_to_target_signal_to_noise(cls, array, pixel_scale, target_signal_to_noise, exposure_time_map,
                                           psf=None, background_sky_map=None, seed=-1):
        """
        Create a realistic simulated image by applying effects to a plain simulated image.

        Parameters
        ----------
        target_signal_to_noise
        array : ndarray
            The image before simulating (e.g. the lens and source galaxies before optics blurring and CCD read-out).
        pixel_scale: float
            The scale of each pixel in arc seconds
        exposure_time_map : ndarray
            An array representing the effective exposure time of each pixel.
        psf: PSF
            An array describing the PSF the simulated image is blurred with.
        background_sky_map : ndarray
            The value of background sky in every image pixel (electrons per second).
        seed: int
            A seed for random noise_maps generation
        """

        max_index = np.unravel_index(array.argmax(), array.shape)
        max_image = array[max_index]
        max_effective_exposure_time = exposure_time_map[max_index]
        max_array_counts = np.multiply(max_image, max_effective_exposure_time)
        if background_sky_map is not None:
            max_background_sky_map = background_sky_map[max_index]
            max_background_sky_map_counts = np.multiply(max_background_sky_map, max_effective_exposure_time)
        else:
            max_background_sky_map_counts = None

        scale_factor = 1.

        if background_sky_map is None:
            scale_factor = target_signal_to_noise ** 2.0 / max_array_counts
        elif background_sky_map is not None:
            scale_factor = (max_array_counts + max_background_sky_map_counts) * target_signal_to_noise ** 2.0 \
                           / max_array_counts ** 2.0

        scaled_effective_exposure_time = np.multiply(scale_factor, exposure_time_map)

        return cls.simulate_variable_arrays(array=array, pixel_scale=pixel_scale,
                                            exposure_time_map=scaled_effective_exposure_time,
                                            psf=psf, background_sky_map=background_sky_map,
                                            add_noise=True, noise_seed=seed)