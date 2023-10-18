def pdw_period_find(times,
                    mags,
                    errs,
                    autofreq=True,
                    init_p=None,
                    end_p=None,
                    f_step=1.0e-4,
                    phasebinsize=None,
                    sigclip=10.0,
                    nworkers=None,
                    verbose=False):
    '''This is the parallel version of the function above.

    Uses the string length method in Dworetsky 1983 to calculate the period of a
    time-series of magnitude measurements and associated magnitude errors. This
    can optionally bin in phase to try to speed up the calculation.

    PARAMETERS:

    time: series of times at which mags were measured (usually some form of JD)
    mag: timeseries of magnitudes (np.array)
    err: associated errs per magnitude measurement (np.array)
    init_p, end_p: interval to search for periods between (both ends inclusive)
    f_step: step in frequency [days^-1] to use

    RETURNS:

    tuple of the following form:

    (periods (np.array),
     string_lengths (np.array),
     good_period_mask (boolean array))

    '''

    # remove nans
    find = npisfinite(times) & npisfinite(mags) & npisfinite(errs)
    ftimes, fmags, ferrs = times[find], mags[find], errs[find]

    mod_mags = (fmags - npmin(fmags))/(2.0*(npmax(fmags) - npmin(fmags))) - 0.25

    if len(ftimes) > 9 and len(fmags) > 9 and len(ferrs) > 9:

        # get the median and stdev = 1.483 x MAD
        median_mag = np.median(fmags)
        stddev_mag = (np.median(np.abs(fmags - median_mag))) * 1.483

        # sigclip next
        if sigclip:

            sigind = (np.abs(fmags - median_mag)) < (sigclip * stddev_mag)

            stimes = ftimes[sigind]
            smags = fmags[sigind]
            serrs = ferrs[sigind]

            LOGINFO('sigclip = %s: before = %s observations, '
                    'after = %s observations' %
                    (sigclip, len(times), len(stimes)))

        else:

            stimes = ftimes
            smags = fmags
            serrs = ferrs

        # make sure there are enough points to calculate a spectrum
        if len(stimes) > 9 and len(smags) > 9 and len(serrs) > 9:

            # get the frequencies to use
            if init_p:
                endf = 1.0/init_p
            else:
                # default start period is 0.1 day
                endf = 1.0/0.1

            if end_p:
                startf = 1.0/end_p
            else:
                # default end period is length of time series
                startf = 1.0/(stimes.max() - stimes.min())

            # if we're not using autofreq, then use the provided frequencies
            if not autofreq:
                frequencies = np.arange(startf, endf, stepsize)
                LOGINFO(
                    'using %s frequency points, start P = %.3f, end P = %.3f' %
                    (frequencies.size, 1.0/endf, 1.0/startf)
                )
            else:
                # this gets an automatic grid of frequencies to use
                frequencies = get_frequency_grid(stimes,
                                                 minfreq=startf,
                                                 maxfreq=endf)
                LOGINFO(
                    'using autofreq with %s frequency points, '
                    'start P = %.3f, end P = %.3f' %
                    (frequencies.size,
                     1.0/frequencies.max(),
                     1.0/frequencies.min())
                )


            # set up some internal stuff
            fold_time = npmin(ftimes) # fold at the first time element
            j_range = len(fmags)-1
            epsilon = 2.0 * npmean(ferrs)
            delta_l = 0.34 * (epsilon - 0.5*(epsilon**2)) * (len(ftimes) -
                                                             npsqrt(10.0/epsilon))
            keep_threshold_1 = 1.6 + 1.2*delta_l
            l = 0.212*len(ftimes)
            sig_l = len(ftimes)/37.5
            keep_threshold_2 = l + 4.0*sig_l

            # generate the tasks
            tasks = [(x,
                      ftimes,
                      mod_mags,
                      fold_time,
                      j_range,
                      keep_threshold_1,
                      keep_threshold_2,
                      phasebinsize) for x in frequencies]

            # fire up the pool and farm out the tasks
            if (not nworkers) or (nworkers > NCPUS):
                nworkers = NCPUS
                LOGINFO('using %s workers...' % nworkers)

            pool = Pool(nworkers)
            strlen_results = pool.map(pdw_worker, tasks)
            pool.close()
            pool.join()
            del pool

            periods, strlens, goodflags = zip(*strlen_results)
            periods, strlens, goodflags = (np.array(periods),
                                           np.array(strlens),
                                           np.array(goodflags))

            strlensort = npargsort(strlens)
            nbeststrlens = strlens[strlensort[:5]]
            nbestperiods = periods[strlensort[:5]]
            nbestflags = goodflags[strlensort[:5]]
            bestperiod = nbestperiods[0]
            beststrlen = nbeststrlens[0]
            bestflag = nbestflags[0]

            return {'bestperiod':bestperiod,
                    'beststrlen':beststrlen,
                    'bestflag':bestflag,
                    'nbeststrlens':nbeststrlens,
                    'nbestperiods':nbestperiods,
                    'nbestflags':nbestflags,
                    'strlens':strlens,
                    'periods':periods,
                    'goodflags':goodflags}

        else:

            LOGERROR('no good detections for these times and mags, skipping...')
            return {'bestperiod':npnan,
                    'beststrlen':npnan,
                    'bestflag':npnan,
                    'nbeststrlens':None,
                    'nbestperiods':None,
                    'nbestflags':None,
                    'strlens':None,
                    'periods':None,
                    'goodflags':None}
    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return {'bestperiod':npnan,
                'beststrlen':npnan,
                'bestflag':npnan,
                'nbeststrlens':None,
                'nbestperiods':None,
                'nbestflags':None,
                'strlens':None,
                'periods':None,
                'goodflags':None}