def mandelagol_fit_magseries(
        times, mags, errs,
        fitparams,
        priorbounds,
        fixedparams,
        trueparams=None,
        burninpercent=0.3,
        plotcorner=False,
        samplesavpath=False,
        n_walkers=50,
        n_mcmc_steps=400,
        eps=1e-4,
        skipsampling=False,
        overwriteexistingsamples=False,
        mcmcprogressbar=False,
        plotfit=False,
        magsarefluxes=False,
        sigclip=10.0,
        verbose=True,
        nworkers=4
):
    '''This fits a Mandel & Agol (2002) planetary transit model to a flux time
    series. You can fit and fix whatever parameters you want.

    It relies on Kreidberg (2015)'s BATMAN implementation for the transit model,
    emcee to sample the posterior (Foreman-Mackey et al 2013), `corner` to plot
    it, and `h5py` to save the samples. See e.g., Claret's work for good guesses
    of star-appropriate limb-darkening parameters.

    NOTE: this only works for flux time-series at the moment.

    NOTE: Between the `fitparams`, `priorbounds`, and `fixedparams` dicts, you
    must specify all of the planetary transit parameters required by BATMAN:
    `['t0', 'rp', 'sma', 'incl', 'u', 'rp', 'ecc', 'omega', 'period']`, or the
    BATMAN model will fail to initialize.

    Parameters
    ----------

    times,mags,errs : np.array
        The input flux time-series to fit a Fourier cosine series to.

    fitparams : dict
        This is the initial parameter guesses for MCMC, found e.g., by
        BLS. The key string format must not be changed, but any parameter can be
        either "fit" or "fixed". If it is "fit", it must have a corresponding
        prior. For example::

            fitparams = {'t0':1325.9, 'rp':np.sqrt(fitd['transitdepth']),
                         'sma':6.17, 'incl':85, 'u':[0.3, 0.2]}

        where 'u' is a list of the limb darkening parameters, Linear first, then
        quadratic. Quadratic limb darkening is the only form implemented.

    priorbounds : dict
        This sets the lower & upper bounds on uniform prior, e.g.::

            priorbounds = {'rp':(0.135, 0.145), 'u_linear':(0.3-1, 0.3+1),
                           'u_quad':(0.2-1, 0.2+1), 't0':(np.min(time),
                           np.max(time)), 'sma':(6,6.4), 'incl':(80,90)}

    fixedparams : dict
        This sets which parameters are fixed, and their values. For example::

            fixedparams = {'ecc':0.,
                           'omega':90.,
                           'limb_dark':'quadratic',
                           'period':fitd['period'] }

        `limb_dark` must be "quadratic".  It's "fixed", because once you
        choose your limb-darkening model, it's fixed.

    trueparams : list of floats
        The true parameter values you're fitting for, if they're known (e.g., a
        known planet, or fake data). Only for plotting purposes.

    burninpercent : float
        The percent of MCMC samples to discard as burn-in.

    plotcorner : str or False
        If this is a str, points to the path of output corner plot that will be
        generated for this MCMC run.

    samplesavpath : str
        This must be provided so `emcee` can save its MCMC samples to disk as
        HDF5 files. This will set the path of the output HDF5file written.

    n_walkers : int
        The number of MCMC walkers to use.

    n_mcmc_steps : int
        The number of MCMC steps to take.

    eps : float
        The radius of the `n_walkers-dimensional` Gaussian ball used to
        initialize the MCMC.

    skipsampling : bool
        If you've already collected MCMC samples, and you do not want any more
        sampling (e.g., just make the plots), set this to be True.

    overwriteexistingsamples : bool
        If you've collected samples, but you want to overwrite them, set this to
        True. Usually, it should be False, which appends samples to
        `samplesavpath` HDF5 file.

    mcmcprogressbar : bool
        If True, will show a progress bar for the MCMC process.

    plotfit: str or bool
        If a str, indicates the path of the output fit plot file. If False, no
        fit plot will be made.

    magsarefluxes : bool
        This indicates if the input measurements in `mags` are actually fluxes.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    verbose : bool
        If True, will indicate MCMC progress.

    nworkers : int
        The number of parallel workers to launch for MCMC.

    Returns
    -------

    dict
        This function returns a dict containing the model fit parameters and
        other fit information. The form of this dict is mostly standardized
        across all functions in this module::

            {
                'fittype':'mandelagol',
                'fitinfo':{
                    'initialparams':the initial transit params provided,
                    'fixedparams':the fixed transit params provided,
                    'finalparams':the final model fit transit params,
                    'finalparamerrs':formal errors in the params,
                    'fitmags': the model fit mags,
                    'fitepoch': the epoch of minimum light for the fit,
                },
                'fitplotfile': the output fit plot if fitplot is not None,
                'magseries':{
                    'times':input times in phase order of the model,
                    'phase':the phases of the model mags,
                    'mags':input mags/fluxes in the phase order of the model,
                    'errs':errs in the phase order of the model,
                    'magsarefluxes':input value of magsarefluxes kwarg
                }
            }

    '''

    from multiprocessing import Pool
    fittype = 'mandelagol'

    if not magsarefluxes:
        raise NotImplementedError('magsarefluxes is not implemented yet.')
    if not samplesavpath:
        raise ValueError(
            'This function requires that you save the samples somewhere'
        )
    if not mandel_agol_dependencies:
        raise ImportError(
            'This function depends on BATMAN, emcee>3.0, corner, and h5py.'
        )

    # sigma clip and get rid of zero errs
    stimes, smags, serrs = sigclip_magseries(times, mags, errs,
                                             sigclip=sigclip,
                                             magsarefluxes=magsarefluxes)
    nzind = np.nonzero(serrs)
    stimes, smags, serrs = stimes[nzind], smags[nzind], serrs[nzind]

    init_period = _get_value('period', fitparams, fixedparams)
    init_epoch = _get_value('t0', fitparams, fixedparams)
    init_rp = _get_value('rp', fitparams, fixedparams)
    init_sma = _get_value('sma', fitparams, fixedparams)
    init_incl = _get_value('incl', fitparams, fixedparams)
    init_ecc = _get_value('ecc', fitparams, fixedparams)
    init_omega = _get_value('omega', fitparams, fixedparams)
    limb_dark = _get_value('limb_dark', fitparams, fixedparams)
    init_u = _get_value('u', fitparams, fixedparams)

    if not limb_dark == 'quadratic':
        raise ValueError(
            'only quadratic limb-darkening is supported at the moment'
        )

    # initialize the model and calculate the initial model light-curve
    init_params, init_m = _transit_model(stimes, init_epoch, init_period,
                                         init_rp, init_sma, init_incl, init_ecc,
                                         init_omega, init_u, limb_dark)
    init_flux = init_m.light_curve(init_params)

    # guessed initial params. give nice guesses, or else emcee struggles.
    theta, fitparamnames = [], []
    for k in np.sort(list(fitparams.keys())):
        if isinstance(fitparams[k], float) or isinstance(fitparams[k], int):
            theta.append(fitparams[k])
            fitparamnames.append(fitparams[k])
        elif isinstance(fitparams[k], list):
            if not len(fitparams[k]) == 2:
                raise ValueError('should only be quadratic LD coeffs')
            theta.append(fitparams[k][0])
            theta.append(fitparams[k][1])
            fitparamnames.append(fitparams[k][0])
            fitparamnames.append(fitparams[k][1])

    # initialize sampler
    n_dim = len(theta)
    initial_position_vec = [theta + eps*np.random.randn(n_dim)
                            for i in range(n_walkers)]

    # run the MCMC, unless you just want to load the available samples
    if not skipsampling:

        backend = emcee.backends.HDFBackend(samplesavpath)
        if overwriteexistingsamples:
            LOGWARNING(
                'erased samples previously at {:s}'.format(samplesavpath)
            )
            backend.reset(n_walkers, n_dim)

        # if this is the first run, then start from a gaussian ball.
        # otherwise, resume from the previous samples.
        starting_positions = initial_position_vec
        isfirstrun = True
        if os.path.exists(backend.filename):
            if backend.iteration > 1:
                starting_positions = None
                isfirstrun = False

        if verbose and isfirstrun:
            LOGINFO(
                'start {:s} MCMC with {:d} dims, {:d} steps, {:d} walkers,'.
                format(fittype, n_dim, n_mcmc_steps, n_walkers) +
                ' {:d} threads'.format(nworkers)
            )
        elif verbose and not isfirstrun:
            LOGINFO(
                'continue {:s} with {:d} dims, {:d} steps, {:d} walkers, '.
                format(fittype, n_dim, n_mcmc_steps, n_walkers) +
                '{:d} threads'.format(nworkers)
            )

        import sys

        if sys.version_info >= (3, 3):
            with Pool(nworkers) as pool:
                sampler = emcee.EnsembleSampler(
                    n_walkers, n_dim, log_posterior_transit,
                    args=(init_params, init_m, stimes,
                          smags, serrs, priorbounds),
                    pool=pool,
                    backend=backend
                )
                sampler.run_mcmc(starting_positions, n_mcmc_steps,
                                 progress=mcmcprogressbar)

        elif sys.version_info < (3, 3):

            sampler = emcee.EnsembleSampler(
                n_walkers, n_dim, log_posterior_transit,
                args=(init_params, init_m, stimes, smags, serrs, priorbounds),
                threads=nworkers,
                backend=backend
            )
            sampler.run_mcmc(starting_positions, n_mcmc_steps,
                             progress=mcmcprogressbar)

        if verbose:
            LOGINFO(
                'ended {:s} MCMC run with {:d} steps, {:d} walkers, '.format(
                    fittype, n_mcmc_steps, n_walkers
                ) + '{:d} threads'.format(nworkers)
            )

    reader = emcee.backends.HDFBackend(samplesavpath)

    n_to_discard = int(burninpercent*n_mcmc_steps)

    samples = reader.get_chain(discard=n_to_discard, flat=True)
    log_prob_samples = reader.get_log_prob(discard=n_to_discard, flat=True)
    log_prior_samples = reader.get_blobs(discard=n_to_discard, flat=True)

    # Get best-fit parameters and their 1-sigma error bars
    fit_statistics = list(
        map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
            list(zip( *np.percentile(samples, [15.85, 50, 84.15], axis=0))))
    )

    medianparams, std_perrs, std_merrs = {}, {}, {}
    for ix, k in enumerate(np.sort(list(priorbounds.keys()))):
        medianparams[k] = fit_statistics[ix][0]
        std_perrs[k] = fit_statistics[ix][1]
        std_merrs[k] = fit_statistics[ix][2]

    stderrs = {'std_perrs':std_perrs, 'std_merrs':std_merrs}

    per = _get_value('period', medianparams, fixedparams)
    t0 = _get_value('t0', medianparams, fixedparams)
    rp = _get_value('rp', medianparams, fixedparams)
    sma = _get_value('sma', medianparams, fixedparams)
    incl = _get_value('incl', medianparams, fixedparams)
    ecc = _get_value('ecc', medianparams, fixedparams)
    omega = _get_value('omega', medianparams, fixedparams)
    limb_dark = _get_value('limb_dark', medianparams, fixedparams)
    try:
        u = fixedparams['u']
    except Exception as e:
        u = [medianparams['u_linear'], medianparams['u_quad']]

    fit_params, fit_m = _transit_model(stimes, t0, per, rp, sma, incl, ecc,
                                       omega, u, limb_dark)
    fitmags = fit_m.light_curve(fit_params)
    fepoch = t0

    # assemble the return dictionary
    returndict = {
        'fittype':fittype,
        'fitinfo':{
            'initialparams':fitparams,
            'initialmags':init_flux,
            'fixedparams':fixedparams,
            'finalparams':medianparams,
            'finalparamerrs':stderrs,
            'fitmags':fitmags,
            'fitepoch':fepoch,
        },
        'fitplotfile':None,
        'magseries':{
            'times':stimes,
            'mags':smags,
            'errs':serrs,
            'magsarefluxes':magsarefluxes,
        },
    }

    # make the output corner plot, and lightcurve plot if desired
    if plotcorner:
        if isinstance(trueparams,dict):
            trueparamkeys = np.sort(list(trueparams.keys()))
            truelist = [trueparams[k] for k in trueparamkeys]
            fig = corner.corner(
                samples,
                labels=trueparamkeys,
                truths=truelist,
                quantiles=[0.1585, 0.5, .8415], show_titles=True
            )
        else:
            fig = corner.corner(samples,
                                labels=fitparamnames,
                                quantiles=[0.1585, 0.5, .8415],
                                show_titles=True)

        plt.savefig(plotcorner, dpi=300)
        if verbose:
            LOGINFO('saved {:s}'.format(plotcorner))

    if plotfit and isinstance(plotfit, str):

        f, ax = plt.subplots(figsize=(8,6))
        ax.scatter(stimes, smags, c='k', alpha=0.5, label='observed',
                   zorder=1, s=1.5, rasterized=True, linewidths=0)
        ax.scatter(stimes, init_flux, c='r', alpha=1,
                   s=3.5, zorder=2, rasterized=True, linewidths=0,
                   label='initial guess')
        ax.scatter(
            stimes, fitmags, c='b', alpha=1,
            s=1.5, zorder=3, rasterized=True, linewidths=0,
            label='fit {:d} dims'.format(
                len(fitparamnames))
        )
        ax.legend(loc='best')
        ax.set(xlabel='time [days]', ylabel='relative flux')
        f.savefig(plotfit, dpi=300, bbox_inches='tight')
        if verbose:
            LOGINFO('saved {:s}'.format(plotfit))

        returndict['fitplotfile'] = plotfit

    return returndict