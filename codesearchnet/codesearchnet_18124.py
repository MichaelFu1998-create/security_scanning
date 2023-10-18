def optimize_from_initial(s, max_mem=1e9, invert='guess', desc='', rz_order=3,
        min_rad=None, max_rad=None):
    """
    Optimizes a state from an initial set of positions and radii, without
    any known microscope parameters.

    Parameters
    ----------
        s : :class:`peri.states.ImageState`
            The state to optimize. It is modified internally and returned.
        max_mem : Numeric, optional
            The maximum memory for the optimizer to use. Default is 1e9 (bytes)
        invert : Bool or `'guess'`, optional
            Set to True if the image is dark particles on a bright
            background, False otherwise. Used for add-subtract. The
            default is to guess from the state's current particles.
        desc : String, optional
            An additional description to infix for periodic saving along the
            way. Default is the null string ``''``.
        rz_order : int, optional
            ``rz_order`` as passed to opt.burn. Default is 3
        min_rad : Float or None, optional
            The minimum radius to identify a particles as bad, as passed to
            add-subtract. Default is None, which picks half the median radii.
            If your sample is not monodisperse you should pick a different
            value.
        max_rad : Float or None, optional
            The maximum radius to identify a particles as bad, as passed to
            add-subtract. Default is None, which picks 1.5x the median radii.
            If your sample is not monodisperse you should pick a different
            value.

    Returns
    -------
        s : :class:`peri.states.ImageState`
            The optimized state, which is the same as the input ``s`` but
            modified in-place.
    """
    RLOG.info('Initial burn:')
    if desc is not None:
        desc_burn = desc + 'initial-burn'
        desc_polish = desc + 'addsub-polish'
    else:
        desc_burn, desc_polish = [None] * 2
    opt.burn(s, mode='burn', n_loop=3, fractol=0.1, desc=desc_burn,
            max_mem=max_mem, include_rad=False, dowarn=False)
    opt.burn(s, mode='burn', n_loop=3, fractol=0.1, desc=desc_burn,
            max_mem=max_mem, include_rad=True, dowarn=False)

    RLOG.info('Start add-subtract')
    rad = s.obj_get_radii()
    if min_rad is None:
        min_rad = 0.5 * np.median(rad)
    if max_rad is None:
        max_rad = 1.5 * np.median(rad)
    addsub.add_subtract(s, tries=30, min_rad=min_rad, max_rad=max_rad,
            invert=invert)
    if desc is not None:
        states.save(s, desc=desc + 'initial-addsub')

    RLOG.info('Final polish:')
    d = opt.burn(s, mode='polish', n_loop=8, fractol=3e-4, desc=desc_polish,
            max_mem=max_mem, rz_order=rz_order, dowarn=False)
    if not d['converged']:
        RLOG.warn('Optimization did not converge; consider re-running')
    return s