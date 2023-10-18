def finish_state(st, desc='finish-state', invert='guess'):
    """
    Final optimization for the best-possible state.

    Runs a local add-subtract to capture any difficult-to-feature particles,
    then does another set of optimization designed to get to the best
    possible fit.

    Parameters
    ----------
        st : :class:`peri.states.ImageState`
            The state to finish
        desc : String, optional
            Description to intermittently save the state as, as passed to
            state.save. Default is `'finish-state'`.
        invert : {'guess', True, False}
            Whether to invert the image for featuring, as passed to
            addsubtract.add_subtract. Default is to guess from the
            state's current particles.

    See Also
    --------
        `peri.opt.addsubtract.add_subtract_locally`
        `peri.opt.optimize.finish`
    """
    for minmass in [None, 0]:
        for _ in range(3):
            npart, poses = addsub.add_subtract_locally(st, region_depth=7,
                    minmass=minmass, invert=invert)
            if npart == 0:
                break
    opt.finish(st, n_loop=1, separate_psf=True, desc=desc, dowarn=False)
    opt.burn(st, mode='polish', desc=desc, n_loop=2, dowarn=False)
    d = opt.finish(st, desc=desc, n_loop=4, dowarn=False)
    if not d['converged']:
        RLOG.warn('Optimization did not converge; consider re-running')