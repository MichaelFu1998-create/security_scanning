def scaled_noise_map_from_hyper_galaxies_and_contribution_maps(contribution_maps, hyper_galaxies, noise_map):
    """For a contribution map and noise-map, use the model hyper galaxies to compute a scaled noise-map.

    Parameters
    -----------
    contribution_maps : ndarray
        The image's list of 1D masked contribution maps (e.g. one for each hyper galaxy)
    hyper_galaxies : [galaxy.Galaxy]
        The hyper galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the image.
    noise_map : ccd.NoiseMap or ndarray
        An array describing the RMS standard deviation error in each pixel, preferably in units of electrons per
        second.
    """
    scaled_noise_maps = list(map(lambda hyper_galaxy, contribution_map:
                                 hyper_galaxy.hyper_noise_from_contributions(noise_map=noise_map,
                                                                             contributions=contribution_map),
                                 hyper_galaxies, contribution_maps))
    return noise_map + sum(scaled_noise_maps)