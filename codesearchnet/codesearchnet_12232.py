def get_phased_quantities(stimes, smags, serrs, period):
    '''Does phase-folding for the mag/flux time-series given a period.

    Given finite and sigma-clipped times, magnitudes, and errors, along with the
    period at which to phase-fold the data, perform the phase-folding and
    return the phase-folded values.

    Parameters
    ----------

    stimes,smags,serrs : np.array
        The sigma-clipped and finite input mag/flux time-series arrays to
        operate on.

    period : float
        The period to phase the mag/flux time-series at. stimes.min() is used as
        the epoch value to fold the times-series around.

    Returns
    -------

    (phase, pmags, perrs, ptimes, mintime) : tuple
        The tuple returned contains the following items:

        - `phase`: phase-sorted values of phase at each of stimes
        - `pmags`: phase-sorted magnitudes at each phase
        - `perrs`: phase-sorted errors
        - `ptimes`: phase-sorted times
        - `mintime`: earliest time in stimes.

    '''

    # phase the mag series using the given period and faintest mag time
    # mintime = stimes[npwhere(smags == npmax(smags))]

    # phase the mag series using the given period and epoch = min(stimes)
    mintime = np.min(stimes)

    # calculate the unsorted phase, then sort it
    iphase = (stimes - mintime)/period - np.floor((stimes - mintime)/period)
    phasesortind = np.argsort(iphase)

    # these are the final quantities to use for the Fourier fits
    phase = iphase[phasesortind]
    pmags = smags[phasesortind]
    perrs = serrs[phasesortind]

    # get the times sorted in phase order (useful to get the fit mag minimum
    # with respect to phase -- the light curve minimum)
    ptimes = stimes[phasesortind]

    return phase, pmags, perrs, ptimes, mintime