def burn(s, n_loop=6, collect_stats=False, desc='', rz_order=0, fractol=1e-4,
        errtol=1e-2, mode='burn', max_mem=1e9, include_rad=True,
        do_line_min='default', partial_log=False, dowarn=True):
    """
    Optimizes all the parameters of a state.

    Burns a state through calling LMParticleGroupCollection and LMGlobals/
    LMAugmentedState.

    Parameters
    ----------
        s : :class:`peri.states.ImageState`
            The state to optimize
        n_loop : Int, optional
            The number of times to loop over in the optimizer. Default is 6.
        collect_stats : Bool, optional
            Whether or not to collect information on the optimizer's
            performance. Default is False.
        desc : string, optional
            Description to append to the states.save() call every loop.
            Set to None to avoid saving. Default is '', which selects
            one of 'burning', 'polishing', 'doing_positions'
        rz_order: Int, optional
            Set to an int > 0 to optimize with an augmented state (R(z) as
            a global parameter) vs. with the normal global parameters;
            rz_order is the order of the polynomial approximate for R(z).
            Default is 0 (no augmented state).
        fractol : Float, optional
            Fractional change in error at which to terminate. Default 1e-4
        errtol : Float, optional
            Absolute change in error at which to terminate. Default 1e-2
        mode : {'burn', 'do-particles', or 'polish'}, optional
            What mode to optimize with.
            * 'burn'          : Your state is far from the minimum.
            * 'do-particles'  : Positions far from minimum, globals well-fit.
            * 'polish'        : The state is close to the minimum.
            'burn' is the default. Only `polish` will get to the global
            minimum.
        max_mem : Numeric, optional
            The maximum amount of memory allowed for the optimizers' J's,
            for both particles & globals. Default is 1e9, i.e. 1GB per
            optimizer.
        do_line_min : Bool or 'default', optional
            Set to True to do an additional, third optimization per loop
            which optimizes along the subspace spanned by the last 3 steps
            of the burn()'s trajectory. In principle this should signifi-
            cantly speed up the convergence; in practice it sometimes does,
            sometimes doesn't. Default is 'default', which picks by mode:
            * 'burn'          : False
            * 'do-particles'  : False
            * 'polish'        : True
        dowarn : Bool, optional
            Whether to log a warning if termination results from finishing
            loops rather than from convergence. Default is True.

    Returns
    -------
        dictionary
            Dictionary of convergence information. Contains whether the
            optimization has converged (key ``'converged'``), the values of the
            state after each loop (key ``'all_loop_values'``).
            The values of the state's parameters after each part of the
            loop: globals, particles, linemin. If ``collect_stats`` is set,
            then also contains lists of termination dicts from globals,
            particles, and line minimization (keys ``'global_stats'``,
            ``'particle_stats'``, and ``'line_stats``').

    Notes
    -----
    Proceeds by alternating between one Levenberg-Marquardt step
    optimizing the globals, one optimizing the particles, and repeating
    until termination.

    In addition, if `do_line_min` is True, at the end of each loop
    step an additional optimization is tried along the subspaced spanned
    by the steps taken during the last 3 loops. Ideally, this changes the
    convergence from linear to quadratic, but it doesn't always do much.

    Each of the 3 options proceed by optimizing as follows:
    * burn            : lm.do_run_2(), lp.do_run_2(). No psf, 2 loops on lm.
    * do-particles    : lp.do_run_2(), scales for ilm, bkg's
    * polish          : lm.do_run_2(), lp.do_run_2(). Everything, 1 loop each.
    where lm is a globals LMGlobals instance, and lp a
    LMParticleGroupCollection instance.
    """
    # It would be nice if some of these magic #'s (region size,
    # num_eig_dirs, etc) were calculated in a good way. FIXME
    mode = mode.lower()
    if mode not in {'burn', 'do-particles', 'polish'}:
        raise ValueError('mode must be one of burn, do-particles, polish')

    #1. Setting Defaults
    if desc is '':
        desc = mode + 'ing' if mode != 'do-particles' else 'doing-particles'

    eig_update = (mode != 'do-particles')
    glbl_run_length = 3 if mode == 'do-particles' else 6
    glbl_mx_itr = 2 if mode == 'burn' else 1
    use_accel = (mode == 'burn')
    rz_order = int(rz_order)
    if do_line_min == 'default':
        # do_line_min = (mode == 'polish')
        # temporary fix until we solve the particles-leaving-image issue:
        do_line_min = False

    if mode == 'do-particles':
        # FIXME explicit params
        # We pick some parameters for an overall illumination scale:
        glbl_nms = ['ilm-scale', 'ilm-xy-0-0', 'bkg-xy-0-0', 'offset']
        # And now, since we have explicit parameters, we check that they
        # are actually in the state:
        glbl_nms = [nm for nm in glbl_nms if nm in s.params]
    else:
        if mode == 'polish':
            remove_params = None
        else:
            # FIXME explicit params
            remove_params = s.get('psf').params
            if ('zscale' not in remove_params) and ('zscale' in s.params):
                remove_params.append('zscale')
        glbl_nms = name_globals(s, remove_params=remove_params)

    all_lp_stats = []
    all_lm_stats = []
    all_line_stats = []
    all_loop_values = []

    _delta_vals = []  # storing the directions we've moved along for line min
    #2. Optimize
    CLOG.info('Start of loop %d:\t%f' % (0, s.error))
    for a in range(n_loop):
        start_err = s.error
        start_params = np.copy(s.state[s.params])
        #2a. Globals
        # glbl_dmp = 0.3 if a == 0 else 3e-2
        ####FIXME we damp degenerate but convenient spaces in the ilm, bkg
        ####manually, but we should do it more betterer.
        BAD_DAMP = 1e7
        BAD_LIST = [['ilm-scale', BAD_DAMP], ['ilm-off', BAD_DAMP], ['ilm-z-0',
                BAD_DAMP], ['bkg-z-0', BAD_DAMP]]
        ####
        glbl_dmp = vectorize_damping(glbl_nms + ['rz']*rz_order, damping=1.0,
                increase_list=[['psf-', 3e1]] + BAD_LIST)
        if a != 0 or mode != 'do-particles':
            if partial_log:
                log.set_level('debug')
            gstats = do_levmarq(s, glbl_nms, max_iter=glbl_mx_itr, run_length=
                    glbl_run_length, eig_update=eig_update, num_eig_dirs=10,
                    eig_update_frequency=3, rz_order=rz_order, damping=
                    glbl_dmp, decrease_damp_factor=10., use_accel=use_accel,
                    collect_stats=collect_stats, fractol=0.1*fractol,
                    max_mem=max_mem)
            if partial_log:
                log.set_level('info')
            all_lm_stats.append(gstats)
        if desc is not None:
            states.save(s, desc=desc)
        CLOG.info('Globals,   loop {}:\t{}'.format(a, s.error))
        all_loop_values.append(s.values)

        #2b. Particles
        prtl_dmp = 1.0 if a==0 else 1e-2
        #For now, I'm calculating the region size. This might be a bad idea
        #because 1 bad particle can spoil the whole group.
        pstats = do_levmarq_all_particle_groups(s, region_size=40, max_iter=1,
                do_calc_size=True, run_length=4, eig_update=False,
                damping=prtl_dmp, fractol=0.1*fractol, collect_stats=
                collect_stats, max_mem=max_mem, include_rad=include_rad)
        all_lp_stats.append(pstats)
        if desc is not None:
            states.save(s, desc=desc)
        CLOG.info('Particles, loop {}:\t{}'.format(a, s.error))
        gc.collect()
        all_loop_values.append(s.values)

        #2c. Line min?
        end_params = np.copy(s.state[s.params])
        _delta_vals.append(start_params - end_params)
        if do_line_min:
            all_line_stats.append(do_levmarq_n_directions(s, _delta_vals[-3:],
                    collect_stats=collect_stats))
            if desc is not None:
                states.save(s, desc=desc)
            CLOG.info('Line min., loop {}:\t{}'.format(a, s.error))
            all_loop_values.append(s.values)

        #2d. terminate?
        new_err = s.error
        derr = start_err - new_err
        dobreak = (derr/new_err < fractol) or (derr < errtol)
        if dobreak:
            break

    if dowarn and (not dobreak):
        CLOG.warn('burn() did not converge; consider re-running')

    d = {'converged':dobreak, 'all_loop_values':all_loop_values}
    if collect_stats:
        d.update({'global_stats':all_lm_stats, 'particle_stats':all_lp_stats,
                'line_stats':all_line_stats})
    return d