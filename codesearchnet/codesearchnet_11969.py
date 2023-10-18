def time_bin_magseries(times, mags,
                       binsize=540.0,
                       minbinelems=7):
    '''Bins the given mag/flux time-series in time using the bin size given.

    Parameters
    ----------

    times,mags : np.array
        The magnitude/flux time-series to bin in time. Non-finite elements will
        be removed from these arrays. At least 10 elements in each array are
        required for this function to operate.

    binsize : float
        The bin size to use to group together measurements closer than this
        amount in time. This is in seconds.

    minbinelems : int
        The minimum number of elements required per bin to include it in the
        output.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'jdbin_indices': a list of the index arrays into the nan-filtered
                              input arrays per each bin,
             'jdbins': list of bin boundaries for each bin,
             'nbins': the number of bins generated,
             'binnedtimes': the time values associated with each time bin;
                            this is the median of the times in each bin,
             'binnedmags': the mag/flux values associated with each time bin;
                           this is the median of the mags/fluxes in each bin}

    '''

    # check if the input arrays are ok
    if not(times.shape and mags.shape and len(times) > 9 and len(mags) > 9):

        LOGERROR("input time/mag arrays don't have enough elements")
        return

    # find all the finite values of the magnitudes and times
    finiteind = np.isfinite(mags) & np.isfinite(times)
    finite_times = times[finiteind]
    finite_mags = mags[finiteind]

    # convert binsize in seconds to JD units
    binsizejd = binsize/(86400.0)
    nbins = int(np.ceil((np.nanmax(finite_times) -
                         np.nanmin(finite_times))/binsizejd) + 1)

    minjd = np.nanmin(finite_times)
    jdbins = [(minjd + x*binsizejd) for x in range(nbins)]

    # make a KD-tree on the JDs so we can do fast distance calculations.  we
    # need to add a bogus y coord to make this a problem that KD-trees can
    # solve.
    time_coords = np.array([[x,1.0] for x in finite_times])
    jdtree = cKDTree(time_coords)
    binned_finite_timeseries_indices = []

    collected_binned_mags = {}

    for jd in jdbins:
        # find all bin indices close to within binsizejd of this point
        # using the cKDTree query. we use the p-norm = 1 (I think this
        # means straight-up pairwise distance? FIXME: check this)
        bin_indices = jdtree.query_ball_point(np.array([jd,1.0]),
                                              binsizejd/2.0, p=1.0)

        # if the bin_indices have already been collected, then we're
        # done with this bin, move to the next one. if they haven't,
        # then this is the start of a new bin.
        if (bin_indices not in binned_finite_timeseries_indices and
            len(bin_indices) >= minbinelems):

            binned_finite_timeseries_indices.append(bin_indices)

    # convert to ndarrays
    binned_finite_timeseries_indices = [np.array(x) for x in
                                        binned_finite_timeseries_indices]

    collected_binned_mags['jdbins_indices'] = binned_finite_timeseries_indices
    collected_binned_mags['jdbins'] = jdbins
    collected_binned_mags['nbins'] = len(binned_finite_timeseries_indices)

    # collect the finite_times
    binned_jd = np.array([np.median(finite_times[x])
                          for x in binned_finite_timeseries_indices])
    collected_binned_mags['binnedtimes'] = binned_jd
    collected_binned_mags['binsize'] = binsize

    # median bin the magnitudes according to the calculated indices
    collected_binned_mags['binnedmags'] = (
        np.array([np.median(finite_mags[x])
                  for x in binned_finite_timeseries_indices])
    )

    return collected_binned_mags