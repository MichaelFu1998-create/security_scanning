def finish(s, desc='finish', n_loop=4, max_mem=1e9, separate_psf=True,
        fractol=1e-7, errtol=1e-3, dowarn=True):
    """
    Crawls slowly to the minimum-cost state.

    Blocks the global parameters into small enough sections such that each
    can be optimized separately while including all the pixels (i.e. no
    decimation). Optimizes the globals, then the psf separately if desired,
    then particles, then a line minimization along the step direction to
    speed up convergence.

    Parameters
    ----------
        s : :class:`peri.states.ImageState`
            The state to optimize
        desc : string, optional
            Description to append to the states.save() call every loop.
            Set to `None` to avoid saving. Default is `'finish'`.
        n_loop : Int, optional
            The number of times to loop over in the optimizer. Default is 4.
        max_mem : Numeric, optional
            The maximum amount of memory allowed for the optimizers' J's,
            for both particles & globals. Default is 1e9.
        separate_psf : Bool, optional
            If True, does the psf optimization separately from the rest of
            the globals, since the psf has a more tortuous fit landscape.
            Default is True.
        fractol : Float, optional
            Fractional change in error at which to terminate. Default 1e-4
        errtol : Float, optional
            Absolute change in error at which to terminate. Default 1e-2
        dowarn : Bool, optional
            Whether to log a warning if termination results from finishing
            loops rather than from convergence. Default is True.

    Returns
    -------
        dictionary
            Information about the optimization. Has two keys: ``'converged'``,
            a Bool which of whether optimization stopped due to convergence
            (True) or due to max number of iterations (False), and
            ``'loop_values'``, a [n_loop+1, N] ``numpy.ndarray`` of the
            state's values, at the start of optimization and at the end of
            each loop, before the line minimization.
    """
    values = [np.copy(s.state[s.params])]
    remove_params = s.get('psf').params if separate_psf else None
    # FIXME explicit params
    global_params = name_globals(s, remove_params=remove_params)
    #FIXME this could be done much better, since much of the globals such
    #as the ilm are local. Could be done with sparse matrices and/or taking
    #nearby globals in a group and using the update tile only as the slicer,
    #rather than the full residuals.
    gs = np.floor(max_mem / s.residuals.nbytes).astype('int')
    groups = [global_params[a:a+gs] for a in range(0, len(global_params), gs)]
    CLOG.info('Start  ``finish``:\t{}'.format(s.error))
    for a in range(n_loop):
        start_err = s.error
        #1. Min globals:
        for g in groups:
            do_levmarq(s, g, damping=0.1, decrease_damp_factor=20.,
                    max_iter=1, max_mem=max_mem, eig_update=False)
        if separate_psf:
            do_levmarq(s, remove_params, max_mem=max_mem, max_iter=4,
                    eig_update=False)
        CLOG.info('Globals,   loop {}:\t{}'.format(a, s.error))
        if desc is not None:
            states.save(s, desc=desc)
        #2. Min particles
        do_levmarq_all_particle_groups(s, max_iter=1, max_mem=max_mem)
        CLOG.info('Particles, loop {}:\t{}'.format(a, s.error))
        if desc is not None:
            states.save(s, desc=desc)
        #3. Append vals, line min:
        values.append(np.copy(s.state[s.params]))
        # dv = (np.array(values[1:]) - np.array(values[0]))[-3:]
        # do_levmarq_n_directions(s, dv, damping=1e-2, max_iter=2, errtol=3e-4)
        # CLOG.info('Line min., loop {}:\t{}'.format(a, s.error))
        # if desc is not None:
            # states.save(s, desc=desc)
        #4. terminate?
        new_err = s.error
        derr = start_err - new_err
        dobreak = (derr/new_err < fractol) or (derr < errtol)
        if dobreak:
            break

    if dowarn and (not dobreak):
        CLOG.warn('finish() did not converge; consider re-running')
    return {'converged':dobreak, 'loop_values':np.array(values)}