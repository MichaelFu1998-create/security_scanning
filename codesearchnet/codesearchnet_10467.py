def galaxies_in_redshift_ordered_planes_from_galaxies(galaxies, plane_redshifts):
    """Given a list of galaxies (with redshifts), return a list of the galaxies where each entry contains a list \
    of galaxies at the same redshift in ascending redshift order.

    Parameters
    -----------
    galaxies : [Galaxy]
        The list of galaxies in the ray-tracing calculation.
    """

    galaxies_in_redshift_ordered_planes =  [[] for i in range(len(plane_redshifts))]

    for galaxy in galaxies:

        index = (np.abs(np.asarray(plane_redshifts) - galaxy.redshift)).argmin()

        galaxies_in_redshift_ordered_planes[index].append(galaxy)

    return galaxies_in_redshift_ordered_planes