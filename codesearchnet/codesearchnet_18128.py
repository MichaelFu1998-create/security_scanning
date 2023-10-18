def _translate_particles(s, max_mem=1e9, desc='', min_rad='calc',
        max_rad='calc', invert='guess', rz_order=0, do_polish=True):
    """
    Workhorse for translating particles. See get_particles_featuring for docs.
    """
    if desc is not None:
        desc_trans = desc + 'translate-particles'
        desc_burn = desc + 'addsub_burn'
        desc_polish = desc + 'addsub_polish'
    else:
        desc_trans, desc_burn, desc_polish = [None]*3
    RLOG.info('Translate Particles:')
    opt.burn(s, mode='do-particles', n_loop=4, fractol=0.1, desc=desc_trans,
            max_mem=max_mem, include_rad=False, dowarn=False)
    opt.burn(s, mode='do-particles', n_loop=4, fractol=0.05, desc=desc_trans,
            max_mem=max_mem, include_rad=True, dowarn=False)

    RLOG.info('Start add-subtract')
    addsub.add_subtract(s, tries=30, min_rad=min_rad, max_rad=max_rad,
        invert=invert)
    if desc is not None:
        states.save(s, desc=desc + 'translate-addsub')

    if do_polish:
        RLOG.info('Final Burn:')
        opt.burn(s, mode='burn', n_loop=3, fractol=3e-4, desc=desc_burn,
                max_mem=max_mem, rz_order=rz_order,dowarn=False)
        RLOG.info('Final Polish:')
        d = opt.burn(s, mode='polish', n_loop=4, fractol=3e-4, desc=desc_polish,
                max_mem=max_mem, rz_order=rz_order, dowarn=False)
        if not d['converged']:
            RLOG.warn('Optimization did not converge; consider re-running')