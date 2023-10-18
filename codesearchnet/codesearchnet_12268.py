def bls_snr(blsdict,
            times,
            mags,
            errs,
            assumeserialbls=False,
            magsarefluxes=False,
            sigclip=10.0,
            npeaks=None,
            perioddeltapercent=10,
            ingressdurationfraction=0.1,
            verbose=True):
    '''Calculates the signal to noise ratio for each best peak in the BLS
    periodogram, along with transit depth, duration, and refit period and epoch.

    The following equation is used for SNR::

        SNR = (transit model depth / RMS of LC with transit model subtracted)
              * sqrt(number of points in transit)

    Parameters
    ----------

    blsdict : dict
        This is an lspinfo dict produced by either `bls_parallel_pfind` or
        `bls_serial_pfind` in this module, or by your own BLS function. If you
        provide results in a dict from an external BLS function, make sure this
        matches the form below::

            {'bestperiod': the best period value in the periodogram,
             'bestlspval': the periodogram peak associated with the best period,
             'nbestpeaks': the input value of nbestpeaks,
             'nbestlspvals': nbestpeaks-size list of best period peak values,
             'nbestperiods': nbestpeaks-size list of best periods,
             'lspvals': the full array of periodogram powers,
             'frequencies': the full array of frequencies considered,
             'periods': the full array of periods considered,
             'blsresult': list of result dicts from eebls.f wrapper functions,
             'stepsize': the actual stepsize used,
             'nfreq': the actual nfreq used,
             'nphasebins': the actual nphasebins used,
             'mintransitduration': the input mintransitduration,
             'maxtransitduration': the input maxtransitdurations,
             'method':'bls' -> the name of the period-finder method,
             'kwargs':{ dict of all of the input kwargs for record-keeping}}

    times,mags,errs : np.array
        These contain the magnitude/flux time-series and any associated errors.

    assumeserialbls : bool
        If this is True, this function will not rerun BLS around each best peak
        in the input lspinfo dict to refit the periods and epochs. This is
        usally required for `bls_parallel_pfind` so set this to False if you use
        results from that function. The parallel method breaks up the frequency
        space into chunks for speed, and the results may not exactly match those
        from a regular BLS run.

    magsarefluxes : bool
        Set to True if the input measurements in `mags` are actually fluxes and
        not magnitudes.

    npeaks : int or None
        This controls how many of the periods in `blsdict['nbestperiods']` to
        find the SNR for. If it's None, then this will calculate the SNR for all
        of them. If it's an integer between 1 and
        `len(blsdict['nbestperiods'])`, will calculate for only the specified
        number of peak periods, starting from the best period.

    perioddeltapercent : float
        The fraction of the period provided to use to search around this
        value. This is a percentage. The period range searched will then be::

            [period - (perioddeltapercent/100.0)*period,
             period + (perioddeltapercent/100.0)*period]

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

            {'npeaks: the number of periodogram peaks requested to get SNR for,
             'period': list of refit best periods for each requested peak,
             'epoch': list of refit epochs (i.e. mid-transit times),
             'snr':list of SNRs of the transit for each requested peak,
             'transitdepth':list of depths of the transits,
             'transitduration':list of durations of the transits,
             'nphasebins':the input value of nphasebins,
             'transingressbin':the phase bin containing transit ingress,
             'transegressbin':the phase bin containing transit egress,
             'allblsmodels':the full BLS models used along with its parameters,
             'allsubtractedmags':BLS models - phased light curves,
             'allphasedmags':the phase light curves,
             'allphases': the phase values}

    '''

    # figure out how many periods to work on
    if (npeaks and (0 < npeaks < len(blsdict['nbestperiods']))):
        nperiods = npeaks
    else:
        if verbose:
            LOGWARNING('npeaks not specified or invalid, '
                       'getting SNR for all %s BLS peaks' %
                       len(blsdict['nbestperiods']))
        nperiods = len(blsdict['nbestperiods'])

    nbestperiods = blsdict['nbestperiods'][:nperiods]

    # get rid of nans first and sigclip
    stimes, smags, serrs = sigclip_magseries(times,
                                             mags,
                                             errs,
                                             magsarefluxes=magsarefluxes,
                                             sigclip=sigclip)


    # make sure there are enough points to calculate a spectrum
    if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

        nbestsnrs = []
        transitdepth, transitduration = [], []
        nphasebins, transingressbin, transegressbin = [], [], []

        # keep these around for diagnostics
        allsubtractedmags = []
        allphasedmags = []
        allphases = []
        allblsmodels = []

        # these are refit periods and epochs
        refitperiods = []
        refitepochs = []

        for period in nbestperiods:

            # get the period interval
            startp = period - perioddeltapercent*period/100.0

            if startp < 0:
                startp = period

            endp = period + perioddeltapercent*period/100.0

            # see if we need to rerun bls_serial_pfind
            if not assumeserialbls:

                # run bls_serial_pfind with the kwargs copied over from the
                # initial run. replace only the startp, endp, verbose, sigclip
                # kwarg values
                prevkwargs = blsdict['kwargs'].copy()
                prevkwargs['verbose'] = verbose
                prevkwargs['startp'] = startp
                prevkwargs['endp'] = endp
                prevkwargs['sigclip'] = None

                blsres = bls_serial_pfind(stimes,
                                          smags,
                                          serrs,
                                          **prevkwargs)

            else:
                blsres = blsdict

            thistransdepth = blsres['blsresult']['transdepth']
            thistransduration = blsres['blsresult']['transduration']
            thisbestperiod = blsres['bestperiod']
            thistransingressbin = blsres['blsresult']['transingressbin']
            thistransegressbin = blsres['blsresult']['transegressbin']
            thisnphasebins = blsdict['kwargs']['nphasebins']

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


            # update the lists with results from this peak
            nbestsnrs.append(stats['snr'])
            transitdepth.append(stats['transitdepth'])
            transitduration.append(stats['transitduration'])
            transingressbin.append(stats['transingressbin'])
            transegressbin.append(stats['transegressbin'])
            nphasebins.append(stats['nphasebins'])

            # update the refit periods and epochs
            refitperiods.append(stats['period'])
            refitepochs.append(stats['epoch'])

            # update the diagnostics
            allsubtractedmags.append(stats['subtractedmags'])
            allphasedmags.append(stats['phasedmags'])
            allphases.append(stats['phases'])
            allblsmodels.append(stats['blsmodel'])

        # done with working on each peak

    # if there aren't enough points in the mag series, bail out
    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        nbestsnrs = None
        transitdepth, transitduration = None, None
        nphasebins, transingressbin, transegressbin = None, None, None
        allsubtractedmags, allphases, allphasedmags = None, None, None

    return {'npeaks':npeaks,
            'period':refitperiods,
            'epoch':refitepochs,
            'snr':nbestsnrs,
            'transitdepth':transitdepth,
            'transitduration':transitduration,
            'nphasebins':nphasebins,
            'transingressbin':transingressbin,
            'transegressbin':transegressbin,
            'allblsmodels':allblsmodels,
            'allsubtractedmags':allsubtractedmags,
            'allphasedmags':allphasedmags,
            'allphases':allphases}