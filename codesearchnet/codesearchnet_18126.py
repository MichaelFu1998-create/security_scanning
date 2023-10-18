def get_particles_featuring(feature_rad, state_name=None, im_name=None,
        use_full_path=False, actual_rad=None, invert=True, featuring_params={},
        **kwargs):
    """
    Combines centroid featuring with the globals from a previous state.

    Runs trackpy.locate on an image, sets the globals from a previous state,
    calls _translate_particles

    Parameters
    ----------
        feature_rad : Int, odd
            The particle radius for featuring, as passed to locate_spheres.

        state_name : String or None, optional
            The name of the initially-optimized state. Default is None,
            which prompts the user to select the name interactively
            through a Tk window.
        im_name : String or None, optional
            The name of the new image to optimize. Default is None,
            which prompts the user to select the name interactively
            through a Tk window.
        use_full_path : Bool, optional
            Set to True to use the full path of the state instead of
            partial path names (e.g. /full/path/name/state.pkl vs
            state.pkl). Default is False
        actual_rad : Float or None, optional
            The initial guess for the particle radii. Default is the median
            of the previous state.
        invert : Bool
            Whether to invert the image for featuring, as passed to
            addsubtract.add_subtract and locate_spheres. Set to False
            if the image is bright particles on a dark background.
            Default is True (dark particles on bright background).
        featuring_params : Dict, optional
            kwargs-like dict of any additional keyword arguments to pass to
            ``get_initial_featuring``, such as ``'use_tp'`` or ``'minmass'``.
            Default is ``{}``.


    Other Parameters
    ----------------
        max_mem : Numeric
            The maximum additional memory to use for the optimizers, as
            passed to optimize.burn. Default is 1e9.
        desc : String, optional
            A description to be inserted in saved state. The save name will
            be, e.g., '0.tif-peri-' + desc + 'initial-burn.pkl'. Default is ''
        min_rad : Float, optional
            The minimum particle radius, as passed to addsubtract.add_subtract.
            Particles with a fitted radius smaller than this are identified
            as fake and removed. Default is 0.5 * actual_rad.
        max_rad : Float, optional
            The maximum particle radius, as passed to addsubtract.add_subtract.
            Particles with a fitted radius larger than this are identified
            as fake and removed. Default is 1.5 * actual_rad, however you
            may find better results if you make this more stringent.
        rz_order : int, optional
            If nonzero, the order of an additional augmented rscl(z)
            parameter for optimization. Default is 0; i.e. no rscl(z)
            optimization.
        do_polish : Bool, optional
            Set to False to only optimize the particles and add-subtract.
            Default is True, which then runs a polish afterwards.

    Returns
    -------
        s : :class:`peri.states.ImageState`
            The optimized state.

    See Also
    --------
        get_initial_featuring   : Features an image from scratch, using
            centroid methods as initial particle locations.

        feature_from_pos_rad    : Using a previous state's globals and
            user-provided positions and radii as an initial guess,
            completely optimizes a state.

        translate_featuring     : Use a previous state's globals and
            centroids methods for an initial particle guess, completely
            optimizes a state.

    Notes
    -----
        The ``Other Parameters`` are passed to _translate_particles.
    Proceeds by:
        1. Find a guess of the particle positions through centroid methods.
        2. Optimize particle positions only.
        3. Optimize particle positions and radii only.
        4. Add-subtract missing and bad particles.
        5. If polish, optimize the illumination, background, and particles.
        6. If polish, optimize everything.
    """
    state_name, im_name = _pick_state_im_name(
            state_name, im_name, use_full_path=use_full_path)
    s = states.load(state_name)

    if actual_rad is None:
        actual_rad = np.median(s.obj_get_radii())
    im = util.RawImage(im_name, tile=s.image.tile)
    pos = locate_spheres(im, feature_rad, invert=invert, **featuring_params)
    _ = s.obj_remove_particle(np.arange(s.obj_get_radii().size))
    s.obj_add_particle(pos, np.ones(pos.shape[0])*actual_rad)

    s.set_image(im)
    _translate_particles(s, invert=invert, **kwargs)
    return s