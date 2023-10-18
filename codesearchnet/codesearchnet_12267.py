def bls_stats_singleperiod(times, mags, errs, period,
                           magsarefluxes=False,
                           sigclip=10.0,
                           perioddeltapercent=10,
                           nphasebins=200,
                           mintransitduration=0.01,
                           maxtransitduration=0.4,
                           ingressdurationfraction=0.1,
                           verbose=True):
    '''This calculates the SNR, depth, duration, a refit period, and time of
    center-transit for a single period.

    The equation used for SNR is::

        SNR = (transit model depth / RMS of LC with transit model subtracted)
              * sqrt(number of points in transit)

    NOTE: you should set the kwargs `sigclip`, `nphasebins`,
    `mintransitduration`, `maxtransitduration` to what you used for an initial
    BLS run to detect transits in the input light curve to match those input
    conditions.

    Parameters
    ----------

    times,mags,errs : np.array
        These contain the magnitude/flux time-series and any associated errors.

    period : float
        The period to search around and refit the transits. This will be used to
        calculate the start and end periods of a rerun of BLS to calculate the
        stats.

    magsarefluxes : bool
        Set to True if the input measurements in `mags` are actually fluxes and
        not magnitudes.

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

    perioddeltapercent : float
        The fraction of the period provided to use to search around this
        value. This is a percentage. The period range searched will then be::

            [period - (perioddeltapercent/100.0)*period,
             period + (perioddeltapercent/100.0)*period]

    nphasebins : int
        The number of phase bins to use in the BLS run.

    mintransitduration : float
        The minimum transit duration in phase to consider.

    maxtransitduration : float
        The maximum transit duration to consider.

    ingressdurationfraction : float
        The fraction of the transit duration to use to generate an initial value
        of the transit ingress duration for the BLS model refit. This will be
        fit by this function.

    verbose : bool
        If True, will indicate progress and any problems encountered.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'period': the refit best period,
             'epoch': the refit epoch (i.e. mid-transit time),
             'snr':the SNR of the transit,
             'transitdepth':the depth of the transit,
             'transitduration':the duration of the transit,
             'nphasebins':the input value of nphasebins,
             'transingressbin':the phase bin containing transit ingress,
             'transegressbin':the phase bin containing transit egress,
             'blsmodel':the full BLS model used along with its parameters,
             'subtractedmags':BLS model - phased light curve,
             'phasedmags':the phase light curve,
             'phases': the phase values}

    '''

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        # get the period interval
        startp = period - perioddeltapercent*period/100.0

        if startp < 0:
            startp = period

        endp = period + perioddeltapercent*period/100.0

        # rerun BLS in serial mode around the specified period to get the
        # transit depth, duration, ingress and egress bins
        blsres = bls_serial_pfind(stimes, smags, serrs,
                                  verbose=verbose,
                                  startp=startp,
                                  endp=endp,
                                  nphasebins=nphasebins,
                                  mintransitduration=mintransitduration,
                                  maxtransitduration=maxtransitduration,
                                  magsarefluxes=magsarefluxes,
                                  get_stats=False,
                                  sigclip=None)

        if (not blsres or
            'blsresult' not in blsres or
            blsres['blsresult'] is None):
            LOGERROR("BLS failed during a period-search "
                     "performed around the input best period: %.6f. "
                     "Can't continue. " % period)
            return None

        thistransdepth = blsres['blsresult']['transdepth']
        thistransduration = blsres['blsresult']['transduration']
        thisbestperiod = blsres['bestperiod']
        thistransingressbin = blsres['blsresult']['transingressbin']
        thistransegressbin = blsres['blsresult']['transegressbin']
        thisnphasebins = nphasebins

        stats = _get_bls_stats(stimes,
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
                               magsarefluxes=magsarefluxes,
                               verbose=verbose)

        return stats


    # if there aren't enough points in the mag series, bail out
    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return None