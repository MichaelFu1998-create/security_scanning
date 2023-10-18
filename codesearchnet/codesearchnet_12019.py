def scipylsp_parallel(times,
                      mags,
                      errs, # ignored but for consistent API
                      startp,
                      endp,
                      nbestpeaks=5,
                      periodepsilon=0.1, # 0.1
                      stepsize=1.0e-4,
                      nworkers=4,
                      sigclip=None,
                      timebin=None):
    '''
    This uses the LSP function from the scipy library, which is fast as hell. We
    try to make it faster by running LSP for sections of the omegas array in
    parallel.

    '''

    # make sure there are no nans anywhere
    finiteind = np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[finiteind], mags[finiteind], errs[finiteind]

    if len(ftimes) > 0 and len(fmags) > 0:

        # sigclip the lightcurve if asked to do so
        if sigclip:
            worktimes, workmags, _ = sigclip_magseries(ftimes,
                                                       fmags,
                                                       ferrs,
                                                       sigclip=sigclip)
            LOGINFO('ndet after sigclipping = %s' % len(worktimes))

        else:
            worktimes = ftimes
            workmags = fmags

        # bin the lightcurve if asked to do so
        if timebin:

            binned = time_bin_magseries(worktimes, workmags, binsize=timebin)
            worktimes = binned['binnedtimes']
            workmags = binned['binnedmags']

        # renormalize the working mags to zero and scale them so that the
        # variance = 1 for use with our LSP functions
        normmags = (workmags - np.median(workmags))/np.std(workmags)

        startf = 1.0/endp
        endf = 1.0/startp
        omegas = 2*np.pi*np.arange(startf, endf, stepsize)

        # partition the omegas array by nworkers
        tasks = []
        chunksize = int(float(len(omegas))/nworkers) + 1
        tasks = [omegas[x*chunksize:x*chunksize+chunksize]
                 for x in range(nworkers)]

        # map to parallel workers
        if (not nworkers) or (nworkers > NCPUS):
            nworkers = NCPUS
            LOGINFO('using %s workers...' % nworkers)

        pool = Pool(nworkers)

        tasks = [(worktimes, normmags, x) for x in tasks]
        lsp = pool.map(parallel_scipylsp_worker, tasks)

        pool.close()
        pool.join()

        lsp = np.concatenate(lsp)
        periods = 2.0*np.pi/omegas

        # find the nbestpeaks for the periodogram: 1. sort the lsp array by
        # highest value first 2. go down the values until we find five values
        # that are separated by at least periodepsilon in period

        # make sure we only get finite lsp values
        finitepeakind = npisfinite(lsp)
        finlsp = lsp[finitepeakind]
        finperiods = periods[finitepeakind]

        bestperiodind = npargmax(finlsp)

        sortedlspind = np.argsort(finlsp)[::-1]
        sortedlspperiods = finperiods[sortedlspind]
        sortedlspvals = finlsp[sortedlspind]

        prevbestlspval = sortedlspvals[0]
        # now get the nbestpeaks
        nbestperiods, nbestlspvals, peakcount = (
            [finperiods[bestperiodind]],
            [finlsp[bestperiodind]],
            1
        )
        prevperiod = sortedlspperiods[0]

        # find the best nbestpeaks in the lsp and their periods
        for period, lspval in zip(sortedlspperiods, sortedlspvals):

            if peakcount == nbestpeaks:
                break
            perioddiff = abs(period - prevperiod)
            bestperiodsdiff = [abs(period - x) for x in nbestperiods]

            # print('prevperiod = %s, thisperiod = %s, '
            #       'perioddiff = %s, peakcount = %s' %
            #       (prevperiod, period, perioddiff, peakcount))

            # this ensures that this period is different from the last period
            # and from all the other existing best periods by periodepsilon to
            # make sure we jump to an entire different peak in the periodogram
            if (perioddiff > periodepsilon and
                all(x > periodepsilon for x in bestperiodsdiff)):
                nbestperiods.append(period)
                nbestlspvals.append(lspval)
                peakcount = peakcount + 1

            prevperiod = period


        return {'bestperiod':finperiods[bestperiodind],
                'bestlspval':finlsp[bestperiodind],
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':nbestlspvals,
                'nbestperiods':nbestperiods,
                'lspvals':lsp,
                'omegas':omegas,
                'periods':periods,
                'method':'sls'}

    else:

        LOGERROR('no good detections for these times and mags, skipping...')
        return {'bestperiod':npnan,
                'bestlspval':npnan,
                'nbestpeaks':nbestpeaks,
                'nbestlspvals':None,
                'nbestperiods':None,
                'lspvals':None,
                'periods':None,
                'method':'sls'}