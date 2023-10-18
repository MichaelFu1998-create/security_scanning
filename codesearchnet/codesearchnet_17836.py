def add_missing_particles(st, rad='calc', tries=50, **kwargs):
    """
    Attempts to add missing particles to the state.

    Operates by:
    (1) featuring the difference image using feature_guess,
    (2) attempting to add the featured positions using check_add_particles.

    Parameters
    ----------
    st : :class:`peri.states.State`
        The state to check adding particles to.
    rad : Float or 'calc', optional
        The radius of the newly-added particles and of the feature size for
        featuring. Default is 'calc', which uses the median of the state's
        current radii.
    tries : Int, optional
        How many particles to attempt to add. Only tries to add the first
        ``tries`` particles, in order of mass. Default is 50.

    Other Parameters
    ----------------
    invert : Bool, optional
        Whether to invert the image. Default is ``True``, i.e. dark particles
    minmass : Float or None, optionals
        The minimum mass/masscut of a particle. Default is ``None``=calcualted
        by ``feature_guess``.
    use_tp : Bool, optional
        Whether to use trackpy in feature_guess. Default is False, since
        trackpy cuts out particles at the edge.

    do_opt : Bool, optional
        Whether to optimize the particle position before checking if it
        should be kept. Default is True (optimizes position).
    im_change_frac : Float, optional
        How good the change in error needs to be relative to the change
        in the difference image. Default is 0.2; i.e. if the error does
        not decrease by 20% of the change in the difference image, do
        not add the particle.

    min_derr : Float or '3sig', optional
        The minimal improvement in error to add a particle. Default
        is ``'3sig' = 3*st.sigma``.

    Returns
    -------
    accepts : Int
        The number of added particles
    new_poses : [N,3] list
        List of the positions of the added particles. If ``do_opt==True``,
        then these positions will differ from the input 'guess'.
    """
    if rad == 'calc':
        rad = guess_add_radii(st)

    guess, npart = feature_guess(st, rad, **kwargs)
    tries = np.min([tries, npart])

    accepts, new_poses = check_add_particles(
        st, guess[:tries], rad=rad, **kwargs)
    return accepts, new_poses