def phase_bin_magseries(phases, mags,
                        binsize=0.005,
                        minbinelems=7):
    '''Bins a phased magnitude/flux time-series using the bin size provided.

    Parameters
    ----------

    phases,mags : np.array
        The phased magnitude/flux time-series to bin in phase. Non-finite
        elements will be removed from these arrays. At least 10 elements in each
        array are required for this function to operate.

    binsize : float
        The bin size to use to group together measurements closer than this
        amount in phase. This is in units of phase.

    minbinelems : int
        The minimum number of elements required per bin to include it in the
        output.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'phasebin_indices': a list of the index arrays into the
                                 nan-filtered input arrays per each bin,
             'phasebins': list of bin boundaries for each bin,
             'nbins': the number of bins generated,
             'binnedphases': the phase values associated with each phase bin;
                            this is the median of the phase value in each bin,
             'binnedmags': the mag/flux values associated with each phase bin;
                           this is the median of the mags/fluxes in each bin}

    '''

    # check if the input arrays are ok
    if not(phases.shape and mags.shape and len(phases) > 10 and len(mags) > 10):

        LOGERROR("input time/mag arrays don't have enough elements")
        return

    # find all the finite values of the magnitudes and phases
    finiteind = np.isfinite(mags) & np.isfinite(phases)
    finite_phases = phases[finiteind]
    finite_mags = mags[finiteind]

    nbins = int(np.ceil((np.nanmax(finite_phases) -
                         np.nanmin(finite_phases))/binsize) + 1)

    minphase = np.nanmin(finite_phases)
    phasebins = [(minphase + x*binsize) for x in range(nbins)]

    # make a KD-tree on the PHASEs so we can do fast distance calculations.  we
    # need to add a bogus y coord to make this a problem that KD-trees can
    # solve.
    time_coords = np.array([[x,1.0] for x in finite_phases])
    phasetree = cKDTree(time_coords)
    binned_finite_phaseseries_indices = []

    collected_binned_mags = {}

    for phase in phasebins:

        # find all bin indices close to within binsize of this point using the
        # cKDTree query. we use the p-norm = 1 for pairwise Euclidean distance.
        bin_indices = phasetree.query_ball_point(np.array([phase,1.0]),
                                                 binsize/2.0, p=1.0)

        # if the bin_indices have already been collected, then we're
        # done with this bin, move to the next one. if they haven't,
        # then this is the start of a new bin.
        if (bin_indices not in binned_finite_phaseseries_indices and
            len(bin_indices) >= minbinelems):

            binned_finite_phaseseries_indices.append(bin_indices)

    # convert to ndarrays
    binned_finite_phaseseries_indices = [np.array(x) for x in
                                         binned_finite_phaseseries_indices]

    collected_binned_mags['phasebins_indices'] = (
        binned_finite_phaseseries_indices
    )
    collected_binned_mags['phasebins'] = phasebins
    collected_binned_mags['nbins'] = len(binned_finite_phaseseries_indices)

    # collect the finite_phases
    binned_phase = np.array([np.median(finite_phases[x])
                             for x in binned_finite_phaseseries_indices])
    collected_binned_mags['binnedphases'] = binned_phase
    collected_binned_mags['binsize'] = binsize

    # median bin the magnitudes according to the calculated indices
    collected_binned_mags['binnedmags'] = (
        np.array([np.median(finite_mags[x])
                  for x in binned_finite_phaseseries_indices])
    )

    return collected_binned_mags