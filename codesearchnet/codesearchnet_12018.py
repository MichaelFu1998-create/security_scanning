def parallel_townsend_lsp(times, mags, startp, endp,
                          stepsize=1.0e-4,
                          nworkers=4):
    '''
    This calculates the Lomb-Scargle periodogram for the frequencies
    corresponding to the period interval (startp, endp) using a frequency step
    size of stepsize cycles/day. This uses the algorithm in Townsend 2010.

    '''

    # make sure there are no nans anywhere
    finiteind = np.isfinite(times) & np.isfinite(mags)
    ftimes, fmags = times[finiteind], mags[finiteind]

    # renormalize the mags to zero and scale them so that the variance = 1
    nmags = (fmags - np.median(fmags))/np.std(fmags)

    startf = 1.0/endp
    endf = 1.0/startp
    omegas = 2*np.pi*np.arange(startf, endf, stepsize)

    # parallel map the lsp calculations
    if (not nworkers) or (nworkers > NCPUS):
        nworkers = NCPUS
        LOGINFO('using %s workers...' % nworkers)

    pool = Pool(nworkers)

    tasks = [(ftimes, nmags, x) for x in omegas]
    lsp = pool.map(townsend_lombscargle_wrapper, tasks)

    pool.close()
    pool.join()

    return np.array(omegas), np.array(lsp)