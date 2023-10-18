def ordered_plane_redshifts_from_galaxies(galaxies):
    """Given a list of galaxies (with redshifts), return a list of the redshifts in ascending order.

    If two or more galaxies have the same redshift that redshift is not double counted.

    Parameters
    -----------
    galaxies : [Galaxy]
        The list of galaxies in the ray-tracing calculation.
    """
    ordered_galaxies = sorted(galaxies, key=lambda galaxy: galaxy.redshift, reverse=False)

    # Ideally we'd extract the planes_red_Shfit order from the list above. However, I dont know how to extract it
    # Using a list of class attributes so make a list of redshifts for now.

    galaxy_redshifts = list(map(lambda galaxy: galaxy.redshift, ordered_galaxies))
    return [redshift for i, redshift in enumerate(galaxy_redshifts) if redshift not in galaxy_redshifts[:i]]