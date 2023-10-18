def ordered_plane_redshifts_from_lens_and_source_plane_redshifts_and_slice_sizes(lens_redshifts, planes_between_lenses,
                                                                                 source_plane_redshift):
    """Given a set of lens plane redshifts, the source-plane redshift and the number of planes between each, setup the \
    plane redshifts using these values. A lens redshift corresponds to the 'main' lens galaxy(s),
    whereas the slices collect line-of-sight halos over a range of redshifts.

    The source-plane redshift is removed from the ordered plane redshifts that are returned, so that galaxies are not \
    planed at the source-plane redshift.

    For example, if the main plane redshifts are [1.0, 2.0], and the bin sizes are [1,3], the following redshift \
    slices for planes will be used:

    z=0.5
    z=1.0
    z=1.25
    z=1.5
    z=1.75
    z=2.0

    Parameters
    -----------
    lens_redshifts : [float]
        The redshifts of the main-planes (e.g. the lens galaxy), which determine where redshift intervals are placed.
    planes_between_lenses : [int]
        The number of slices between each main plane. The first entry in this list determines the number of slices \
        between Earth (redshift 0.0) and main plane 0, the next between main planes 0 and 1, etc.
    source_plane_redshift : float
        The redshift of the source-plane, which is input explicitly to ensure galaxies are not placed in the \
        source-plane.
    """

    # Check that the number of slices between lens planes is equal to the number of intervals between the lens planes.
    if len(lens_redshifts) != len(planes_between_lenses)-1:
        raise exc.RayTracingException('The number of lens_plane_redshifts input is not equal to the number of '
                                      'slices_between_lens_planes+1.')

    plane_redshifts = []

    # Add redshift 0.0 and the source plane redshifit to the lens plane redshifts, so that calculation below can use
    # them when dividing slices. These will be removed by the return function at the end from the plane redshifts.

    lens_redshifts.insert(0, 0.0)
    lens_redshifts.append(source_plane_redshift)

    for lens_plane_index in range(1, len(lens_redshifts)):

        previous_plane_redshift = lens_redshifts[lens_plane_index - 1]
        plane_redshift = lens_redshifts[lens_plane_index]
        slice_total = planes_between_lenses[lens_plane_index - 1]
        plane_redshifts += list(np.linspace(previous_plane_redshift, plane_redshift, slice_total+2))[1:]

    return plane_redshifts[0:-1]