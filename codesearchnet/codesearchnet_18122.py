def get_initial_featuring(statemaker, feature_rad, actual_rad=None,
        im_name=None, tile=None, invert=True, desc='', use_full_path=False,
        featuring_params={}, statemaker_kwargs={}, **kwargs):
    """
    Completely optimizes a state from an image of roughly monodisperse
    particles.

    The user can interactively select the image. The state is periodically
    saved during optimization, with different filename for different stages
    of the optimization.

    Parameters
    ----------
        statemaker : Function
            A statemaker function. Given arguments `im` (a
            :class:`~peri.util.Image`), `pos` (numpy.ndarray), `rad` (ndarray),
            and any additional `statemaker_kwargs`, must return a
            :class:`~peri.states.ImageState`.  There is an example function in
            scripts/statemaker_example.py
        feature_rad : Int, odd
            The particle radius for featuring, as passed to locate_spheres.
        actual_rad : Float, optional
            The actual radius of the particles. Default is feature_rad
        im_name : string, optional
            The file name of the image to load. If not set, it is selected
            interactively through Tk.
        tile : :class:`peri.util.Tile`, optional
            The tile of the raw image to be analyzed. Default is None, the
            entire image.
        invert : Bool, optional
            Whether to invert the image for featuring, as passed to trackpy.
            Default is True.
        desc : String, optional
            A description to be inserted in saved state. The save name will
            be, e.g., '0.tif-peri-' + desc + 'initial-burn.pkl'. Default is ''
        use_full_path : Bool, optional
            Set to True to use the full path name for the image. Default
            is False.
        featuring_params : Dict, optional
            kwargs-like dict of any additional keyword arguments to pass to
            ``get_initial_featuring``, such as ``'use_tp'`` or ``'minmass'``.
            Default is ``{}``.
        statemaker_kwargs : Dict, optional
            kwargs-like dict of any additional keyword arguments to pass to
            the statemaker function. Default is ``{}``.

    Other Parameters
    ----------------
        max_mem : Numeric
            The maximum additional memory to use for the optimizers, as
            passed to optimize.burn. Default is 1e9.
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
        zscale : Float, optional
            The zscale of the image. Default is 1.0

    Returns
    -------
        s : :class:`peri.states.ImageState`
            The optimized state.

    See Also
    --------
        feature_from_pos_rad    : Using a previous state's globals and
            user-provided positions and radii as an initial guess,
            completely optimizes a state.

        get_particle_featuring  : Using a previous state's globals and
            positions as an initial guess, completely optimizes a state.

        translate_featuring     : Use a previous state's globals and
            centroids methods for an initial particle guess, completely
            optimizes a state.

    Notes
    -----
    Proceeds by centroid-featuring the image for an initial guess of
    particle positions, then optimizing the globals + positions until
    termination as called in _optimize_from_centroid.
    The ``Other Parameters`` are passed to _optimize_from_centroid.
    """
    if actual_rad is None:
        actual_rad = feature_rad

    _,  im_name = _pick_state_im_name('', im_name, use_full_path=use_full_path)
    im = util.RawImage(im_name, tile=tile)

    pos = locate_spheres(im, feature_rad, invert=invert, **featuring_params)
    if np.size(pos) == 0:
        msg = 'No particles found. Try using a smaller `feature_rad`.'
        raise ValueError(msg)

    rad = np.ones(pos.shape[0], dtype='float') * actual_rad
    s = statemaker(im, pos, rad, **statemaker_kwargs)
    RLOG.info('State Created.')
    if desc is not None:
        states.save(s, desc=desc+'initial')
    optimize_from_initial(s, invert=invert, desc=desc, **kwargs)
    return s