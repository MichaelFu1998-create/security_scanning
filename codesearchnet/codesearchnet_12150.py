def lcfit_features(times, mags, errs, period,
                   fourierorder=5,
                   # these are depth, duration, ingress duration
                   transitparams=(-0.01,0.1,0.1),
                   # these are depth, duration, depth ratio, secphase
                   ebparams=(-0.2,0.3,0.7,0.5),
                   sigclip=10.0,
                   magsarefluxes=False,
                   fitfailure_means_featurenan=False,
                   verbose=True):
    '''This calculates various features related to fitting models to light
    curves.

    This function:

    - calculates `R_ij` and `phi_ij` ratios for Fourier fit amplitudes and
      phases.

    - calculates the reduced chi-sq for fourier, EB, and planet transit fits.

    - calculates the reduced chi-sq for fourier, EB, planet transit fits w/2 x
      period.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to calculate periodic features for.

    period : float
        The period of variabiity to use to phase the light curve.

    fourierorder : int
        The Fourier order to use to generate sinusoidal function and fit that to
        the phased light curve.

    transitparams : list of floats
        The transit depth, duration, and ingress duration to use to generate a
        trapezoid planet transit model fit to the phased light curve. The period
        used is the one provided in `period`, while the epoch is automatically
        obtained from a spline fit to the phased light curve.

    ebparams : list of floats
        The primary eclipse depth, eclipse duration, the primary-secondary depth
        ratio, and the phase of the secondary eclipse to use to generate an
        eclipsing binary model fit to the phased light curve. The period used is
        the one provided in `period`, while the epoch is automatically obtained
        from a spline fit to the phased light curve.

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

    magsarefluxes : bool
        Set this to True if the input measurements in `mags` are actually
        fluxes.

    fitfailure_means_featurenan : bool
        If the planet, EB and EBx2 fits don't return standard errors because the
        covariance matrix could not be generated, then the fit is suspicious and
        the features calculated can't be trusted. If
        `fitfailure_means_featurenan` is True, then the output features for
        these fits will be set to nan.

    verbose : bool
        If True, will indicate progress while working.

    Returns
    -------

    dict
        A dict of all the features calculated is returned.

    '''

    # get the finite values
    finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[finind], mags[finind], errs[finind]

    # get nonzero errors
    nzind = np.nonzero(ferrs)
    ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

    # get the MAD of the unphased light curve
    lightcurve_median = np.median(fmags)
    lightcurve_mad = np.median(np.abs(fmags - lightcurve_median))

    #
    # fourier fit
    #

    # we fit a Fourier series to the light curve using the best period and
    # extract the amplitudes and phases up to the 8th order to fit the LC. the
    # various ratios of the amplitudes A_ij and the differences in the phases
    # phi_ij are also used as periodic variability features

    # do the fit
    ffit = lcfit.fourier_fit_magseries(ftimes, fmags, ferrs, period,
                                       fourierorder=fourierorder,
                                       sigclip=sigclip,
                                       magsarefluxes=magsarefluxes,
                                       verbose=verbose)

    # get the coeffs and redchisq
    fourier_fitcoeffs = ffit['fitinfo']['finalparams']
    fourier_chisq = ffit['fitchisq']
    fourier_redchisq = ffit['fitredchisq']

    if fourier_fitcoeffs is not None:

        fourier_modelmags, _, _, fpmags, _ = sinusoidal.fourier_sinusoidal_func(
            [period,
             ffit['fitinfo']['fitepoch'],
             ffit['fitinfo']['finalparams'][:fourierorder],
             ffit['fitinfo']['finalparams'][fourierorder:]],
            ftimes,
            fmags,
            ferrs
        )

        fourier_residuals = fourier_modelmags - fpmags
        fourier_residual_median = np.median(fourier_residuals)
        fourier_residual_mad = np.median(np.abs(fourier_residuals -
                                                fourier_residual_median))


        # break them out into amps and phases
        famplitudes = fourier_fitcoeffs[:fourierorder]
        fphases = fourier_fitcoeffs[fourierorder:]

        famp_combos = combinations(famplitudes,2)
        famp_cinds = combinations(range(len(famplitudes)),2)

        fpha_combos = combinations(fphases,2)
        fpha_cinds = combinations(range(len(fphases)),2)

    else:

        LOGERROR('LC fit to sinusoidal series model failed, '
                 'using initial params')

        initfourieramps = [0.6] + [0.2]*(fourierorder - 1)
        initfourierphas = [0.1] + [0.1]*(fourierorder - 1)

        fourier_modelmags, _, _, fpmags, _ = sinusoidal.fourier_sinusoidal_func(
            [period,
             ffit['fitinfo']['fitepoch'],
             initfourieramps,
             initfourierphas],
            ftimes,
            fmags,
            ferrs
        )

        fourier_residuals = fourier_modelmags - fpmags
        fourier_residual_median = np.median(fourier_residuals)
        fourier_residual_mad = np.median(np.abs(fourier_residuals -
                                                fourier_residual_median))

        # break them out into amps and phases
        famplitudes = initfourieramps
        fphases = initfourierphas

        famp_combos = combinations(famplitudes,2)
        famp_cinds = combinations(range(len(famplitudes)),2)

        fpha_combos = combinations(fphases,2)
        fpha_cinds = combinations(range(len(fphases)),2)


    fampratios = {}
    fphadiffs = {}

    # get the ratios for all fourier coeff combinations
    for ampi, ampc, phai, phac in zip(famp_cinds,
                                      famp_combos,
                                      fpha_cinds,
                                      fpha_combos):

        ampratind = 'R_%s%s' % (ampi[1]+1, ampi[0]+1)
        # this is R_ij
        amprat = ampc[1]/ampc[0]
        phadiffind = 'phi_%s%s' % (phai[1]+1, phai[0]+1)
        # this is phi_ij
        phadiff = phac[1] - phai[0]*phac[0]

        fampratios[ampratind] = amprat
        fphadiffs[phadiffind] = phadiff

    # update the outdict for the Fourier fit results
    outdict = {
        'fourier_ampratios':fampratios,
        'fourier_phadiffs':fphadiffs,
        'fourier_fitparams':fourier_fitcoeffs,
        'fourier_redchisq':fourier_redchisq,
        'fourier_chisq':fourier_chisq,
        'fourier_residual_median':fourier_residual_median,
        'fourier_residual_mad':fourier_residual_mad,
        'fourier_residual_mad_over_lcmad':fourier_residual_mad/lightcurve_mad
    }

    # EB and planet fits will find the epoch automatically
    planetfitparams = [period,
                       None,
                       transitparams[0],
                       transitparams[1],
                       transitparams[2]]

    ebfitparams = [period,
                   None,
                   ebparams[0],
                   ebparams[1],
                   ebparams[2],
                   ebparams[3]]

    # do the planet and EB fit with this period
    planet_fit = lcfit.traptransit_fit_magseries(ftimes, fmags, ferrs,
                                                 planetfitparams,
                                                 sigclip=sigclip,
                                                 magsarefluxes=magsarefluxes,
                                                 verbose=verbose)

    planetfit_finalparams = planet_fit['fitinfo']['finalparams']

    planetfit_finalparamerrs = planet_fit['fitinfo']['finalparamerrs']

    if planetfit_finalparamerrs is None and fitfailure_means_featurenan:

        LOGWARNING('planet fit: no standard errors available '
                   'for fit parameters, fit is bad, '
                   'setting fit chisq and red-chisq to np.nan')
        planetfit_chisq = np.nan
        planetfit_redchisq = np.nan
        planet_residual_median = np.nan
        planet_residual_mad = np.nan
        planet_residual_mad_over_lcmad = np.nan

    else:

        planetfit_chisq = planet_fit['fitchisq']
        planetfit_redchisq = planet_fit['fitredchisq']

        if planetfit_finalparams is not None:

            planet_modelmags, _, _, ppmags, _ = transits.trapezoid_transit_func(
                planetfit_finalparams,
                ftimes,
                fmags,
                ferrs
            )

        else:

            LOGERROR('LC fit to transit planet model '
                     'failed, using initial params')
            planet_modelmags, _, _, ppmags, _ = transits.trapezoid_transit_func(
                planetfitparams,
                ftimes,
                fmags,
                ferrs
            )

        planet_residuals = planet_modelmags - ppmags
        planet_residual_median = np.median(planet_residuals)
        planet_residual_mad = np.median(np.abs(planet_residuals -
                                               planet_residual_median))
        planet_residual_mad_over_lcmad = planet_residual_mad/lightcurve_mad


    eb_fit = lcfit.gaussianeb_fit_magseries(ftimes, fmags, ferrs,
                                            ebfitparams,
                                            sigclip=sigclip,
                                            magsarefluxes=magsarefluxes,
                                            verbose=verbose)

    ebfit_finalparams = eb_fit['fitinfo']['finalparams']
    ebfit_finalparamerrs = eb_fit['fitinfo']['finalparamerrs']

    if ebfit_finalparamerrs is None and fitfailure_means_featurenan:

        LOGWARNING('EB fit: no standard errors available '
                   'for fit parameters, fit is bad, '
                   'setting fit chisq and red-chisq to np.nan')
        ebfit_chisq = np.nan
        ebfit_redchisq = np.nan
        eb_residual_median = np.nan
        eb_residual_mad = np.nan
        eb_residual_mad_over_lcmad = np.nan

    else:

        ebfit_chisq = eb_fit['fitchisq']
        ebfit_redchisq = eb_fit['fitredchisq']

        if ebfit_finalparams is not None:

            eb_modelmags, _, _, ebpmags, _ = eclipses.invgauss_eclipses_func(
                ebfit_finalparams,
                ftimes,
                fmags,
                ferrs
            )

        else:

            LOGERROR('LC fit to EB model failed, using initial params')

            eb_modelmags, _, _, ebpmags, _ = eclipses.invgauss_eclipses_func(
                ebfitparams,
                ftimes,
                fmags,
                ferrs
            )

        eb_residuals = eb_modelmags - ebpmags
        eb_residual_median = np.median(eb_residuals)
        eb_residual_mad = np.median(np.abs(eb_residuals - eb_residual_median))
        eb_residual_mad_over_lcmad = eb_residual_mad/lightcurve_mad


    # do the EB fit with 2 x period
    ebfitparams[0] = ebfitparams[0]*2.0
    eb_fitx2 = lcfit.gaussianeb_fit_magseries(ftimes, fmags, ferrs,
                                              ebfitparams,
                                              sigclip=sigclip,
                                              magsarefluxes=magsarefluxes,
                                              verbose=verbose)

    ebfitx2_finalparams = eb_fitx2['fitinfo']['finalparams']
    ebfitx2_finalparamerrs = eb_fitx2['fitinfo']['finalparamerrs']

    if ebfitx2_finalparamerrs is None and fitfailure_means_featurenan:

        LOGWARNING('EB x2 period fit: no standard errors available '
                   'for fit parameters, fit is bad, '
                   'setting fit chisq and red-chisq to np.nan')
        ebfitx2_chisq = np.nan
        ebfitx2_redchisq = np.nan
        ebx2_residual_median = np.nan
        ebx2_residual_mad = np.nan
        ebx2_residual_mad_over_lcmad = np.nan

    else:

        ebfitx2_chisq = eb_fitx2['fitchisq']
        ebfitx2_redchisq = eb_fitx2['fitredchisq']

        if ebfitx2_finalparams is not None:

            ebx2_modelmags, _, _, ebx2pmags, _ = (
                eclipses.invgauss_eclipses_func(
                    ebfitx2_finalparams,
                    ftimes,
                    fmags,
                    ferrs
                )
            )

        else:

            LOGERROR('LC fit to EB model with 2xP failed, using initial params')

            ebx2_modelmags, _, _, ebx2pmags, _ = (
                eclipses.invgauss_eclipses_func(
                    ebfitparams,
                    ftimes,
                    fmags,
                    ferrs
                )
            )

        ebx2_residuals = ebx2_modelmags - ebx2pmags
        ebx2_residual_median = np.median(ebx2_residuals)
        ebx2_residual_mad = np.median(np.abs(ebx2_residuals -
                                             ebx2_residual_median))

        ebx2_residual_mad_over_lcmad = ebx2_residual_mad/lightcurve_mad


    # update the outdict
    outdict.update({
        'planet_fitparams':planetfit_finalparams,
        'planet_chisq':planetfit_chisq,
        'planet_redchisq':planetfit_redchisq,
        'planet_residual_median':planet_residual_median,
        'planet_residual_mad':planet_residual_mad,
        'planet_residual_mad_over_lcmad':(
            planet_residual_mad_over_lcmad,
        ),
        'eb_fitparams':ebfit_finalparams,
        'eb_chisq':ebfit_chisq,
        'eb_redchisq':ebfit_redchisq,
        'eb_residual_median':eb_residual_median,
        'eb_residual_mad':eb_residual_mad,
        'eb_residual_mad_over_lcmad':(
            eb_residual_mad_over_lcmad,
        ),
        'ebx2_fitparams':ebfitx2_finalparams,
        'ebx2_chisq':ebfitx2_chisq,
        'ebx2_redchisq':ebfitx2_redchisq,
        'ebx2_residual_median':ebx2_residual_median,
        'ebx2_residual_mad':ebx2_residual_mad,
        'ebx2_residual_mad_over_lcmad':(
            ebx2_residual_mad_over_lcmad,
        ),
    })

    return outdict