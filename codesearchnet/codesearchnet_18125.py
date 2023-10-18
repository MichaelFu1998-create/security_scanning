def translate_featuring(state_name=None, im_name=None, use_full_path=False,
        **kwargs):
    """
    Translates one optimized state into another image where the particles
    have moved by a small amount (~1 particle radius).

    Returns a completely-optimized state. The user can interactively
    selects the initial state and the second raw image. The state is
    periodically saved during optimization, with different filename for
    different stages of the optimization.

    Parameters
    ----------
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
        invert : {True, False, 'guess'}
            Whether to invert the image for featuring, as passed to
            addsubtract.add_subtract. Default is to guess from the
            state's current particles.
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

        get_particle_featuring  : Using a previous state's globals and
            positions as an initial guess, completely optimizes a state.

    Notes
    -----
    The ``Other Parameters`` are passed to _translate_particles.
    Proceeds by:
        1. Optimize particle positions only.
        2. Optimize particle positions and radii only.
        3. Add-subtract missing and bad particles.
        4. If polish, optimize the illumination, background, and particles.
        5. If polish, optimize everything.
    """
    state_name, im_name = _pick_state_im_name(
            state_name, im_name, use_full_path=use_full_path)

    s = states.load(state_name)
    im = util.RawImage(im_name, tile=s.image.tile)

    s.set_image(im)
    _translate_particles(s, **kwargs)
    return s