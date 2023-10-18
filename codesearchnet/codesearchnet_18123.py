def feature_from_pos_rad(statemaker, pos, rad, im_name=None, tile=None,
        desc='', use_full_path=False, statemaker_kwargs={}, **kwargs):
    """
    Gets a completely-optimized state from an image and an initial guess of
    particle positions and radii.

    The state is periodically saved during optimization, with different
    filename for different stages of the optimization. The user can select
    the image.

    Parameters
    ----------
        statemaker : Function
            A statemaker function. Given arguments `im` (a
            :class:`~peri.util.Image`), `pos` (numpy.ndarray), `rad` (ndarray),
            and any additional `statemaker_kwargs`, must return a
            :class:`~peri.states.ImageState`.  There is an example function in
            scripts/statemaker_example.py
        pos : [N,3] element numpy.ndarray.
            The initial guess for the N particle positions.
        rad : N element numpy.ndarray.
            The initial guess for the N particle radii.
        im_name : string or None, optional
            The filename of the image to feature. Default is None, in which
            the user selects the image.
        tile : :class:`peri.util.Tile`, optional
            A tile of the sub-region of the image to feature. Default is
            None, i.e. entire image.
        desc : String, optional
            A description to be inserted in saved state. The save name will
            be, e.g., '0.tif-peri-' + desc + 'initial-burn.pkl'. Default is ''
        use_full_path : Bool, optional
            Set to True to use the full path name for the image. Default
            is False.
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
        invert : {'guess', True, False}
            Whether to invert the image for featuring, as passed to
            addsubtract.add_subtract. Default is to guess from the
            current state's particle positions.
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
        get_initial_featuring   : Features an image from scratch, using
            centroid methods as initial particle locations.

        get_particle_featuring  : Using a previous state's globals and
            positions as an initial guess, completely optimizes a state.

        translate_featuring     : Use a previous state's globals and
            centroids methods for an initial particle guess, completely
            optimizes a state.

    Notes
    -----
    The ``Other Parameters`` are passed to _optimize_from_centroid.
    Proceeds by centroid-featuring the image for an initial guess of
    particle positions, then optimizing the globals + positions until
    termination as called in _optimize_from_centroid.
    """
    if np.size(pos) == 0:
        raise ValueError('`pos` is an empty array.')
    elif np.shape(pos)[1] != 3:
        raise ValueError('`pos` must be an [N,3] element numpy.ndarray.')
    _,  im_name = _pick_state_im_name('', im_name, use_full_path=use_full_path)
    im = util.RawImage(im_name, tile=tile)
    s = statemaker(im, pos, rad, **statemaker_kwargs)
    RLOG.info('State Created.')
    if desc is not None:
        states.save(s, desc=desc+'initial')
    optimize_from_initial(s, desc=desc, **kwargs)
    return s