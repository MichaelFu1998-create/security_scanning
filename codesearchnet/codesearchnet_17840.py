def add_subtract_misfeatured_tile(
        st, tile, rad='calc', max_iter=3, invert='guess', max_allowed_remove=20,
        minmass=None, use_tp=False, **kwargs):
    """
    Automatically adds and subtracts missing & extra particles in a region
    of poor fit.

    Parameters
    ----------
    st: :class:`peri.states.State`
        The state to add and subtract particles to.
    tile : :class:`peri.util.Tile`
        The poorly-fit region to examine.
    rad : Float or 'calc', optional
        The initial radius for added particles; added particles radii are
        not fit until the end of add_subtract. Default is ``'calc'``, which
        uses the median radii of active particles.
    max_iter : Int, optional
        The maximum number of loops for attempted adds at one tile location.
        Default is 3.
    invert : {'guess', True, False}, optional
        Whether to invert the image for feature_guess -- True for dark
        particles on a bright background, False for bright particles. The
        default is to guess from the state's current particles.
    max_allowed_remove : Int, optional
        The maximum number of particles to remove. If the misfeatured tile
        contains more than this many particles, raises an error. If it
        contains more than half as many particles, logs a warning. If more
        than this many particles are added, they are optimized in blocks of
        ``max_allowed_remove``. Default is 20.

    Other Parameters
    ----------------
    im_change_frac : Float on [0, 1], optional.
        If adding or removing a particle decreases the error less than
        ``im_change_frac``*the change in the image, the particle is deleted.
        Default is 0.2.

    min_derr : {Float, ``'3sig'``}, optional
        The minimum change in the state's error to keep a particle in the
        image. Default is ``'3sig'`` which uses ``3*st.sigma``.

    do_opt : Bool, optional
        Set to False to avoid optimizing particle positions after adding
        them. Default is True.

    minmass : Float, optional
        The minimum mass for a particle to be identified as a feature, as
        used by trackpy. Defaults to a decent guess.

    use_tp : Bool, optional
        Set to True to use trackpy to find missing particles inside the
        image. Not recommended since trackpy deliberately cuts out particles
        at the edge of the image. Default is False.

    Outputs
    -------
    n_added : Int
        The change in the number of particles, i.e. ``n_added-n_subtracted``
    ainds: List of ints
        The indices of the added particles.

    Notes
    --------
    The added/removed positions returned are whether or not the
    position has been added or removed ever. It's possible/probably that
    a position is added, then removed during a later iteration.

    Algorithm is:
    1.  Remove all particles within the tile.
    2.  Feature and add particles to the tile.
    3.  Optimize the added particles positions only.
    4.  Run 2-3 until no particles have been added.
    5.  Optimize added particle radii
    Because all the particles are removed within a tile, it is important
    to set max_allowed_remove to a reasonable value. Otherwise, if the
    tile is the size of the image it can take a long time to remove all
    the particles and re-add them.
    """
    if rad == 'calc':
        rad = guess_add_radii(st)
    if invert == 'guess':
        invert = guess_invert(st)
    # 1. Remove all possibly bad particles within the tile.
    initial_error = np.copy(st.error)
    rinds = np.nonzero(tile.contains(st.obj_get_positions()))[0]
    if rinds.size >= max_allowed_remove:
        CLOG.fatal('Misfeatured region too large!')
        raise RuntimeError
    elif rinds.size >= max_allowed_remove/2:
        CLOG.warn('Large misfeatured regions.')
    elif rinds.size > 0:
        rpos, rrad = st.obj_remove_particle(rinds)

    # 2-4. Feature & add particles to the tile, optimize, run until none added
    n_added = -rinds.size
    added_poses = []
    for _ in range(max_iter):
        if invert:
            im = 1 - st.residuals[tile.slicer]
        else:
            im = st.residuals[tile.slicer]
        guess, _ = _feature_guess(im, rad, minmass=minmass, use_tp=use_tp)
        accepts, poses = check_add_particles(
                st, guess+tile.l, rad=rad, do_opt=True, **kwargs)
        added_poses.extend(poses)
        n_added += accepts
        if accepts == 0:
            break
    else:  # for-break-else
        CLOG.warn('Runaway adds or insufficient max_iter')

    # 5. Optimize added pos + rad:
    ainds = []
    for p in added_poses:
        ainds.append(st.obj_closest_particle(p))
    if len(ainds) > max_allowed_remove:
        for i in range(0, len(ainds), max_allowed_remove):
            opt.do_levmarq_particles(
                st, np.array(ainds[i:i + max_allowed_remove]),
                include_rad=True, max_iter=3)
    elif len(ainds) > 0:
        opt.do_levmarq_particles(st, ainds, include_rad=True, max_iter=3)

    # 6. Ensure that current error after add-subtracting is lower than initial
    did_something = (rinds.size > 0) or (len(ainds) > 0)
    if did_something & (st.error > initial_error):
        CLOG.info('Failed addsub, Tile {} -> {}'.format(
            tile.l.tolist(), tile.r.tolist()))
        if len(ainds) > 0:
            _ = st.obj_remove_particle(ainds)
        if rinds.size > 0:
            for p, r in zip(rpos.reshape(-1, 3), rrad.reshape(-1)):
                _ = st.obj_add_particle(p, r)
        n_added = 0
        ainds = []
    return n_added, ainds