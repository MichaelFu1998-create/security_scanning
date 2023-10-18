def contribution_maps_1d_from_hyper_images_and_galaxies(hyper_model_image_1d, hyper_galaxy_images_1d, hyper_galaxies,
                                                        hyper_minimum_values):
    """For a fitting hyper_galaxy_image, hyper_galaxy model image, list of hyper galaxies images and model hyper galaxies, compute
    their contribution maps, which are used to compute a scaled-noise_map map. All quantities are masked 1D arrays.

    The reason this is separate from the *contributions_from_fitting_hyper_images_and_hyper_galaxies* function is that
    each hyper_galaxy image has a list of hyper galaxies images and associated hyper galaxies (one for each galaxy). Thus,
    this function breaks down the calculation of each 1D masked contribution map and returns them in the same datas
    structure (2 lists with indexes [image_index][contribution_map_index].

    Parameters
    ----------
    hyper_model_image_1d : ndarray
        The best-fit model image to the datas (e.g. from a previous analysis phase).
    hyper_galaxy_images_1d : [ndarray]
        The best-fit model image of each hyper galaxy to the datas (e.g. from a previous analysis phase).
    hyper_galaxies : [galaxy.Galaxy]
        The hyper galaxies which represent the model components used to scale the noise_map, which correspond to
        individual galaxies in the image.
    hyper_minimum_values : [float]
        The minimum value of each hyper_galaxy-image contribution map, which ensure zero's don't impact the scaled noise-map.
    """
    # noinspection PyArgumentList
    return list(map(lambda hyper_galaxy, hyper_galaxy_image_1d, hyper_minimum_value:
                    hyper_galaxy.contributions_from_model_image_and_galaxy_image(model_image=hyper_model_image_1d,
                                                                                 galaxy_image=hyper_galaxy_image_1d,
                                                                                 minimum_value=hyper_minimum_value),
                    hyper_galaxies, hyper_galaxy_images_1d, hyper_minimum_values))