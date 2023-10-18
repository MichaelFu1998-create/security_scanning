def add_subtract_locally(st, region_depth=3, filter_size=5, sigma_cutoff=8,
                         **kwargs):
    """
    Automatically adds and subtracts missing particles based on local
    regions of poor fit.

    Calls identify_misfeatured_regions to identify regions, then
    add_subtract_misfeatured_tile on the tiles in order of size until
    region_depth tiles have been checked without adding any particles.

    Parameters
    ----------
    st: :class:`peri.states.State`
        The state to add and subtract particles to.
    region_depth : Int
        The minimum amount of regions to try; the algorithm terminates if
        region_depth regions have been tried without adding particles.

    Other Parameters
    ----------------
    filter_size : Int, optional
        The size of the filter for calculating the local standard deviation;
        should approximately be the size of a poorly featured region in each
        dimension. Best if odd. Default is 5.
    sigma_cutoff : Float, optional
        The max allowed deviation of the residuals from what is expected,
        in units of the residuals' standard deviation. Lower means more
        sensitive, higher = less sensitive. Default is 8.0, i.e. one pixel
        out of every ``7*10^11`` is mis-identified randomly. In practice the
        noise is not Gaussian so there are still some regions mis-
        identified as improperly featured.
    rad : Float or 'calc', optional
        The initial radius for added particles; added particles radii are
        not fit until the end of add_subtract. Default is ``'calc'``, which
        uses the median radii of active particles.
    max_iter : Int, optional
        The maximum number of loops for attempted adds at one tile location.
        Default is 3.
    invert : Bool, optional
        Whether to invert the image for feature_guess. Default is ``True``,
        i.e. dark particles on bright background.
    max_allowed_remove : Int, optional
        The maximum number of particles to remove. If the misfeatured tile
        contains more than this many particles, raises an error. If it
        contains more than half as many particles, throws a warning. If more
        than this many particles are added, they are optimized in blocks of
        ``max_allowed_remove``. Default is 20.
    im_change_frac : Float, between 0 and 1.
        If adding or removing a particle decreases the error less than
        ``im_change_frac *`` the change in the image, the particle is deleted.
        Default is 0.2.
    min_derr : Float
        The minimum change in the state's error to keep a particle in the
        image. Default is ``'3sig'`` which uses ``3*st.sigma``.
    do_opt : Bool, optional
        Set to False to avoid optimizing particle positions after adding
        them. Default is True
    minmass : Float, optional
        The minimum mass for a particle to be identified as a feature, as
        used by trackpy. Defaults to a decent guess.
    use_tp : Bool, optional
        Set to True to use trackpy to find missing particles inside the
        image. Not recommended since trackpy deliberately cuts out
        particles at the edge of the image. Default is False.
    max_allowed_remove : Int, optional
        The maximum number of particles to remove. If the misfeatured tile
        contains more than this many particles, raises an error. If it
        contains more than half as many particles, throws a warning. If more
        than this many particles are added, they are optimized in blocks of
        ``max_allowed_remove``. Default is 20.

    Returns
    -------
    n_added : Int
        The change in the number of particles; i.e the number added - number
        removed.
    new_poses : List
        [N,3] element list of the added particle positions.

    Notes
    -----
    Algorithm Description

    1. Identify mis-featured regions by how much the local residuals
       deviate from the global residuals, as measured by the standard
       deviation of both.
    2. Loop over each of those regions, and:

       a. Remove every particle in the current region.
       b. Try to add particles in the current region until no more
          can be added while adequately decreasing the error.
       c. Terminate if at least region_depth regions have been
          checked without successfully adding a particle.

    Because this algorithm is more judicious about chooosing regions to
    check, and more aggressive about removing particles in those regions,
    it runs faster and does a better job than the (global) add_subtract.
    However, this function usually does not work better as an initial add-
    subtract on an image, since (1) it doesn't check for removing small/big
    particles per se, and (2) when the poorly-featured regions of the image
    are large or when the fit is bad, it will remove essentially all of the
    particles, taking a long time. As a result, it's usually best to do a
    normal add_subtract first and using this function for tough missing or
    double-featured particles.
    """
    # 1. Find regions of poor tiles:
    tiles = identify_misfeatured_regions(
        st, filter_size=filter_size, sigma_cutoff=sigma_cutoff)
    # 2. Add and subtract in the regions:
    n_empty = 0
    n_added = 0
    new_poses = []
    for t in tiles:
        curn, curinds = add_subtract_misfeatured_tile(st, t, **kwargs)
        if curn == 0:
            n_empty += 1
        else:
            n_added += curn
            new_poses.extend(st.obj_get_positions()[curinds])
        if n_empty > region_depth:
            break  # some message or something?
    else:  # for-break-else
        pass
        # CLOG.info('All regions contained particles.')
        # something else?? this is not quite true
    return n_added, new_poses