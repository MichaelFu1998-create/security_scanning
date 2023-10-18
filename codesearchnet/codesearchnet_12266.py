def _get_bls_stats(stimes,
                   smags,
                   serrs,
                   thistransdepth,
                   thistransduration,
                   ingressdurationfraction,
                   nphasebins,
                   thistransingressbin,
                   thistransegressbin,
                   thisbestperiod,
                   thisnphasebins,
                   magsarefluxes=False,
                   verbose=False):
    '''
    Actually calculates the stats.

    '''

    try:

        # try getting the minimum light epoch using the phase bin method
        me_epochbin = int((thistransegressbin +
                           thistransingressbin)/2.0)

        me_phases = (
            (stimes - stimes.min())/thisbestperiod -
            npfloor((stimes - stimes.min())/thisbestperiod)
        )
        me_phases_sortind = npargsort(me_phases)
        me_sorted_phases = me_phases[me_phases_sortind]
        me_sorted_times = stimes[me_phases_sortind]

        me_bins = nplinspace(0.0, 1.0, thisnphasebins)
        me_bininds = npdigitize(me_sorted_phases, me_bins)

        me_centertransit_ind = me_bininds == me_epochbin
        me_centertransit_phase = (
            npmedian(me_sorted_phases[me_centertransit_ind])
        )
        me_centertransit_timeloc = npwhere(
            npabs(me_sorted_phases - me_centertransit_phase) ==
            npmin(npabs(me_sorted_phases - me_centertransit_phase))
        )
        me_centertransit_time = me_sorted_times[
            me_centertransit_timeloc
        ]

        if me_centertransit_time.size > 1:
            LOGWARNING('multiple possible times-of-center transits '
                       'found for period %.7f, picking the first '
                       'one from: %s' %
                       (thisbestperiod, repr(me_centertransit_time)))

        thisminepoch = me_centertransit_time[0]

    except Exception as e:

        LOGEXCEPTION(
            'could not determine the center time of transit for '
            'the phased LC, trying SavGol fit instead...'
        )
        # fit a Savitsky-Golay instead and get its minimum
        savfit = savgol_fit_magseries(stimes, smags, serrs,
                                      thisbestperiod,
                                      magsarefluxes=magsarefluxes,
                                      verbose=verbose,
                                      sigclip=None)
        thisminepoch = savfit['fitinfo']['fitepoch']


    if isinstance(thisminepoch, npndarray):
        if verbose:
            LOGWARNING('minimum epoch is actually an array:\n'
                       '%s\n'
                       'instead of a float, '
                       'are there duplicate time values '
                       'in the original input? '
                       'will use the first value in this array.'
                       % repr(thisminepoch))
        thisminepoch = thisminepoch[0]

    # set up trapezoid transit model to fit for this LC
    transitparams = [
        thisbestperiod,
        thisminepoch,
        thistransdepth,
        thistransduration,
        ingressdurationfraction*thistransduration
    ]

    modelfit = traptransit_fit_magseries(
        stimes,
        smags,
        serrs,
        transitparams,
        sigclip=None,
        magsarefluxes=magsarefluxes,
        verbose=verbose
    )

    # if the model fit succeeds, calculate SNR using the trapezoid model fit
    if modelfit and modelfit['fitinfo']['finalparams'] is not None:

        fitparams = modelfit['fitinfo']['finalparams']
        fiterrs = modelfit['fitinfo']['finalparamerrs']
        modelmags, actualmags, modelphase = (
            modelfit['fitinfo']['fitmags'],
            modelfit['magseries']['mags'],
            modelfit['magseries']['phase']
        )
        subtractedmags = actualmags - modelmags
        subtractedrms = npstd(subtractedmags)
        fit_period, fit_epoch, fit_depth, fit_duration, fit_ingress_dur = (
            fitparams
        )

        npts_in_transit = modelfit['fitinfo']['ntransitpoints']
        transit_snr = (
            npsqrt(npts_in_transit) * npabs(fit_depth/subtractedrms)
        )

        if verbose:

            LOGINFO('refit best period: %.6f, '
                    'refit center of transit: %.5f' %
                    (fit_period, fit_epoch))

            LOGINFO('npoints in transit: %s' % npts_in_transit)

            LOGINFO('transit depth (delta): %.5f, '
                    'frac transit length (q): %.3f, '
                    ' SNR: %.3f' %
                    (fit_depth,
                     fit_duration,
                     transit_snr))

        return {'period':fit_period,
                'epoch':fit_epoch,
                'snr':transit_snr,
                'transitdepth':fit_depth,
                'transitduration':fit_duration,
                'nphasebins':nphasebins,
                'transingressbin':thistransingressbin,
                'transegressbin':thistransegressbin,
                'npoints_in_transit':npts_in_transit,
                'blsmodel':modelmags,
                'subtractedmags':subtractedmags,
                'phasedmags':actualmags,
                'phases':modelphase,
                'fitparams':fitparams,
                'fiterrs':fiterrs,
                'fitinfo':modelfit}


    # if the model fit doesn't work, then do the SNR calculation the old way
    else:

        # phase using this epoch
        phased_magseries = phase_magseries_with_errs(stimes,
                                                     smags,
                                                     serrs,
                                                     thisbestperiod,
                                                     thisminepoch,
                                                     wrap=False,
                                                     sort=True)

        tphase = phased_magseries['phase']
        tmags = phased_magseries['mags']

        # use the transit depth and duration to subtract the BLS transit
        # model from the phased mag series. we're centered about 0.0 as the
        # phase of the transit minimum so we need to look at stuff from
        # [0.0, transitphase] and [1.0-transitphase, 1.0]
        transitphase = thistransduration/2.0

        transitindices = ((tphase < transitphase) |
                          (tphase > (1.0 - transitphase)))

        # this is the BLS model
        # constant = median(tmags) outside transit
        # constant = thistransitdepth inside transit
        blsmodel = npfull_like(tmags, npmedian(tmags))

        if magsarefluxes:

            # eebls.f returns +ve transit depth for fluxes
            # so we need to subtract here to get fainter fluxes in transit
            blsmodel[transitindices] = (
                blsmodel[transitindices] - thistransdepth
            )
        else:

            # eebls.f returns -ve transit depth for magnitudes
            # so we need to subtract here to get fainter mags in transits
            blsmodel[transitindices] = (
                blsmodel[transitindices] - thistransdepth
            )

        # see __init__/get_snr_of_dip docstring for description of transit
        # SNR equation, which is what we use for `thissnr`.
        subtractedmags = tmags - blsmodel
        subtractedrms = npstd(subtractedmags)
        npts_in_transit = len(tmags[transitindices])
        thissnr = (
            npsqrt(npts_in_transit) * npabs(thistransdepth/subtractedrms)
        )

        # tell user about stuff if verbose = True
        if verbose:

            LOGINFO('refit best period: %.6f, '
                    'refit center of transit: %.5f' %
                    (thisbestperiod, thisminepoch))

            LOGINFO('transit ingress phase = %.3f to %.3f' % (1.0 -
                                                              transitphase,
                                                              1.0))
            LOGINFO('transit egress phase = %.3f to %.3f' % (0.0,
                                                             transitphase))
            LOGINFO('npoints in transit: %s' % tmags[transitindices].size)

            LOGINFO('transit depth (delta): %.5f, '
                    'frac transit length (q): %.3f, '
                    ' SNR: %.3f' %
                    (thistransdepth,
                     thistransduration,
                     thissnr))

        return {'period':thisbestperiod,
                'epoch':thisminepoch,
                'snr':thissnr,
                'transitdepth':thistransdepth,
                'transitduration':thistransduration,
                'nphasebins':nphasebins,
                'transingressbin':thistransingressbin,
                'transegressbin':thistransegressbin,
                'blsmodel':blsmodel,
                'subtractedmags':subtractedmags,
                'phasedmags':tmags,
                'phases':tphase}