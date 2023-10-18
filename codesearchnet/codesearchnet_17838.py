def add_subtract(st, max_iter=7, max_npart='calc', max_mem=2e8,
                 always_check_remove=False, **kwargs):
    """
    Automatically adds and subtracts missing & extra particles.

    Operates by removing bad particles then adding missing particles on
    repeat, until either no particles are added/removed or after `max_iter`
    attempts.

    Parameters
    ----------
    st: :class:`peri.states.State`
        The state to add and subtract particles to.
    max_iter : Int, optional
        The maximum number of add-subtract loops to use. Default is 7.
        Terminates after either max_iter loops or when nothing has changed.
    max_npart : Int or 'calc', optional
        The maximum number of particles to add before optimizing the non-psf
        globals. Default is ``'calc'``, which uses 5% of the initial number
        of particles.
    max_mem : Int, optional
        The maximum memory to use for optimization after adding max_npart
        particles. Default is 2e8.
    always_check_remove : Bool, optional
        Set to True to always check whether to remove particles. If ``False``,
        only checks for removal while particles were removed on the previous
        attempt. Default is False.

    Other Parameters
    ----------------
    invert : Bool, optional
        ``True`` if the particles are dark on a bright background, ``False``
        if they are bright on a dark background. Default is ``True``.
    min_rad : Float, optional
        Particles with radius below ``min_rad`` are automatically deleted.
        Default is ``'calc'`` = median rad - 25* radius std.
    max_rad : Float, optional
        Particles with radius above ``max_rad`` are automatically deleted.
        Default is ``'calc'`` = median rad + 15* radius std, but you should
        change this for your particle sizes.

    min_edge_dist : Float, optional
        Particles closer to the edge of the padded image than this are
        automatically deleted. Default is 2.0.
    check_rad_cutoff : 2-element float list.
        Particles with ``radii < check_rad_cutoff[0]`` or ``> check...[1]``
        are checked if they should be deleted (not automatic). Default is
        ``[3.5, 15]``.
    check_outside_im : Bool, optional
        Set to True to check whether to delete particles whose positions are
        outside the un-padded image.

    rad : Float, optional
        The initial radius for added particles; added particles radii are
        not fit until the end of ``add_subtract``. Default is ``'calc'``,
        which uses the median radii of active particles.

    tries : Int, optional
        The number of particles to attempt to remove or add, per iteration.
        Default is 50.

    im_change_frac : Float, optional
        How good the change in error needs to be relative to the change in
        the difference image. Default is 0.2; i.e. if the error does not
        decrease by 20% of the change in the difference image, do not add
        the particle.

    min_derr : Float, optional
        The minimum change in the state's error to keep a particle in the
        image. Default is ``'3sig'`` which uses ``3*st.sigma``.

    do_opt : Bool, optional
        Set to False to avoid optimizing particle positions after adding.
    minmass : Float, optional
        The minimum mass for a particle to be identified as a feature,
        as used by trackpy. Defaults to a decent guess.

    use_tp : Bool, optional
        Set to True to use trackpy to find missing particles inside the
        image. Not recommended since trackpy deliberately cuts out particles
        at the edge of the image. Default is ``False``.

    Returns
    -------
    total_changed : Int
        The total number of adds and subtracts done on the data. Not the
        same as ``changed_inds.size`` since the same particle or particle
        index can be added/subtracted multiple times.
    added_positions : [N_added,3] numpy.ndarray
        The positions of particles that have been added at any point in the
        add-subtract cycle.
    removed_positions : [N_added,3] numpy.ndarray
        The positions of particles that have been removed at any point in
        the add-subtract cycle.

    Notes
    ------
    Occasionally after the intial featuring a cluster of particles is
    featured as 1 big particle. To fix these mistakes, it helps to set
    max_rad to a physical value. This removes the big particle and allows
    it to be re-featured by (several passes of) the adds.

    The added/removed positions returned are whether or not the position
    has been added or removed ever. It's possible that a position is
    added, then removed during a later iteration.
    """
    if max_npart == 'calc':
        max_npart = 0.05 * st.obj_get_positions().shape[0]

    total_changed = 0
    _change_since_opt = 0
    removed_poses = []
    added_poses0 = []
    added_poses = []

    nr = 1  # Check removal on the first loop
    for _ in range(max_iter):
        if (nr != 0) or (always_check_remove):
            nr, rposes = remove_bad_particles(st, **kwargs)
        na, aposes = add_missing_particles(st, **kwargs)
        current_changed = na + nr
        removed_poses.extend(rposes)
        added_poses0.extend(aposes)
        total_changed += current_changed
        _change_since_opt += current_changed
        if current_changed == 0:
            break
        elif _change_since_opt > max_npart:
            _change_since_opt *= 0
            CLOG.info('Start add_subtract optimization.')
            opt.do_levmarq(st, opt.name_globals(st, remove_params=st.get(
                    'psf').params), max_iter=1, run_length=4, num_eig_dirs=3,
                    max_mem=max_mem, eig_update_frequency=2, rz_order=0,
                    use_accel=True)
            CLOG.info('After optimization:\t{:.6}'.format(st.error))

    # Optimize the added particles' radii:
    for p in added_poses0:
        i = st.obj_closest_particle(p)
        opt.do_levmarq_particles(st, np.array([i]), max_iter=2, damping=0.3)
        added_poses.append(st.obj_get_positions()[i])
    return total_changed, np.array(removed_poses), np.array(added_poses)