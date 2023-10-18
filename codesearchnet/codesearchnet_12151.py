def periodogram_features(pgramlist, times, mags, errs,
                         sigclip=10.0,
                         pdiff_threshold=1.0e-4,
                         sidereal_threshold=1.0e-4,
                         sampling_peak_multiplier=5.0,
                         sampling_startp=None,
                         sampling_endp=None,
                         verbose=True):
    '''This calculates various periodogram features (for each periodogram).

    The following features are obtained:

    - For all best periods from all periodogram methods in `pgramlist`,
      calculates the number of these with peaks that are at least
      `sampling_peak_multiplier` x time-sampling periodogram peak at the same
      period. This indicates how likely the `pgramlist` periodogram peaks are to
      being real as opposed to just being caused by time-sampling
      window-function of the observations.

    - For all best periods from all periodogram methods in `pgramlist`,
      calculates the number of best periods which are consistent with a sidereal
      day (1.0027379 and 0.9972696), likely indicating that they're not real.

    - For all best periods from all periodogram methods in `pgramlist`,
      calculates the number of cross-wise period differences for all of these
      that fall below the `pdiff_threshold` value. If this is high, most of the
      period-finders in `pgramlist` agree on their best period results, so it's
      likely the periods found are real.

    Parameters
    ----------

    pgramlist : list of dicts
        This is a list of dicts returned by any of the periodfinding methods in
        :py:mod:`astrobase.periodbase`. This can also be obtained from the
        resulting pickle from the :py:func:astrobase.lcproc.periodsearch.run_pf`
        function. It's a good idea to make `pgramlist` a list of periodogram
        lists from all magnitude columns in the input light curve to test
        periodic variability across all magnitude columns (e.g. period diffs
        between EPD and TFA mags)

    times,mags,errs : np.array
        The input flux/mag time-series to use to calculate features. These are
        used to recalculate the time-sampling L-S periodogram (using
        :py:func:`astrobase.periodbase.zgls.specwindow_lsp`) if one is not
        present in pgramlist. If it's present, these can all be set to None.

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

    pdiff_threshold : float
        This is the max difference between periods to consider them the same.

    sidereal_threshold : float
        This is the max difference between any of the 'best' periods and the
        sidereal day periods to consider them the same.

    sampling_peak_multiplier : float
        This is the minimum multiplicative factor of a 'best' period's
        normalized periodogram peak over the sampling periodogram peak at the
        same period required to accept the 'best' period as possibly real.

    sampling_startp, sampling_endp : float
        If the `pgramlist` doesn't have a time-sampling Lomb-Scargle
        periodogram, it will be obtained automatically. Use these kwargs to
        control the minimum and maximum period interval to be searched when
        generating this periodogram.

    verbose : bool
        If True, will indicate progress and report errors.

    Returns
    -------

    dict
        Returns a dict with all of the periodogram features calculated.

    '''
    # run the sampling peak periodogram if necessary
    pfmethodlist = [pgram['method'] for pgram in pgramlist]

    if 'win' not in pfmethodlist:

        # get the finite values
        finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
        ftimes, fmags, ferrs = times[finind], mags[finind], errs[finind]

        # get nonzero errors
        nzind = np.nonzero(ferrs)
        ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

        sampling_lsp = specwindow_lsp(times, mags, errs,
                                      startp=sampling_startp,
                                      endp=sampling_endp,
                                      sigclip=sigclip,
                                      verbose=verbose)

    else:
        sampling_lsp = pgramlist[pfmethodlist.index('win')]


    # get the normalized sampling periodogram peaks
    normalized_sampling_lspvals = (
        sampling_lsp['lspvals']/(np.nanmax(sampling_lsp['lspvals']) -
                                 np.nanmin(sampling_lsp['lspvals']))
    )
    normalized_sampling_periods = sampling_lsp['periods']

    # go through the periodograms and calculate normalized peak height of best
    # periods over the normalized peak height of the sampling periodogram at the
    # same periods

    for pfm, pgram in zip(pfmethodlist, pgramlist):

        if pfm == 'pdm':

            best_peak_sampling_ratios = []
            close_to_sidereal_flag = []

            periods = pgram['periods']
            peaks = pgram['lspvals']

            normalized_peaks = (1.0 - peaks)/(np.nanmax(1.0 - peaks) -
                                              np.nanmin(1.0 - peaks))

            # get the best period normalized peaks
            if pgram['nbestperiods'] is None:
                LOGERROR('no period results for method: %s' % pfm)
                continue

            for bp in pgram['nbestperiods']:

                if np.isfinite(bp):

                    #
                    # first, get the normalized peak ratio
                    #
                    thisp_norm_pgrampeak = normalized_peaks[periods == bp]

                    thisp_sampling_pgramind = (
                        np.abs(normalized_sampling_periods -
                               bp) < pdiff_threshold
                    )
                    thisp_sampling_peaks = normalized_sampling_lspvals[
                        thisp_sampling_pgramind
                    ]
                    if thisp_sampling_peaks.size > 1:
                        thisp_sampling_ratio = (
                            thisp_norm_pgrampeak/np.mean(thisp_sampling_peaks)
                        )
                    elif thisp_sampling_peaks.size == 1:
                        thisp_sampling_ratio = (
                            thisp_norm_pgrampeak/thisp_sampling_peaks
                        )
                    else:
                        LOGERROR('sampling periodogram is not defined '
                                 'at period %.5f, '
                                 'skipping calculation of ratio' % bp)
                        thisp_sampling_ratio = np.nan

                    best_peak_sampling_ratios.append(thisp_sampling_ratio)

                    #
                    # next, see if the best periods are close to a sidereal day
                    # or any multiples of thus
                    #
                    sidereal_a_ratio = (bp - 1.0027379)/bp
                    sidereal_b_ratio = (bp - 0.9972696)/bp

                    if ((sidereal_a_ratio < sidereal_threshold) or
                        (sidereal_b_ratio < sidereal_threshold)):

                        close_to_sidereal_flag.append(True)

                    else:

                        close_to_sidereal_flag.append(False)



                else:
                    LOGERROR('period is nan')
                    best_peak_sampling_ratios.append(np.nan)
                    close_to_sidereal_flag.append(False)

            # update the pgram with these
            pgram['nbestpeakratios'] = best_peak_sampling_ratios
            pgram['siderealflags'] = close_to_sidereal_flag


        elif pfm != 'win':

            best_peak_sampling_ratios = []
            close_to_sidereal_flag = []

            periods = pgram['periods']
            peaks = pgram['lspvals']

            normalized_peaks = peaks/(np.nanmax(peaks) - np.nanmin(peaks))

            # get the best period normalized peaks
            if pgram['nbestperiods'] is None:
                LOGERROR('no period results for method: %s' % pfm)
                continue

            #
            # first, get the best period normalized peaks
            #
            for bp in pgram['nbestperiods']:

                if np.isfinite(bp):

                    thisp_norm_pgrampeak = normalized_peaks[periods == bp]

                    thisp_sampling_pgramind = (
                        np.abs(normalized_sampling_periods -
                               bp) < pdiff_threshold
                    )
                    thisp_sampling_peaks = normalized_sampling_lspvals[
                        thisp_sampling_pgramind
                    ]
                    if thisp_sampling_peaks.size > 1:
                        thisp_sampling_ratio = (
                            thisp_norm_pgrampeak/np.mean(thisp_sampling_peaks)
                        )
                    elif thisp_sampling_peaks.size == 1:
                        thisp_sampling_ratio = (
                            thisp_norm_pgrampeak/thisp_sampling_peaks
                        )
                    else:
                        LOGERROR('sampling periodogram is not defined '
                                 'at period %.5f, '
                                 'skipping calculation of ratio' % bp)
                        thisp_sampling_ratio = np.nan

                    best_peak_sampling_ratios.append(thisp_sampling_ratio)

                    #
                    # next, see if the best periods are close to a sidereal day
                    # or any multiples of thus
                    #
                    sidereal_a_ratio = (bp - 1.0027379)/bp
                    sidereal_b_ratio = (bp - 0.9972696)/bp

                    if ((sidereal_a_ratio < sidereal_threshold) or
                        (sidereal_b_ratio < sidereal_threshold)):

                        close_to_sidereal_flag.append(True)

                    else:

                        close_to_sidereal_flag.append(False)


                else:
                    LOGERROR('period is nan')
                    best_peak_sampling_ratios.append(np.nan)
                    close_to_sidereal_flag.append(False)

            # update the pgram with these
            pgram['nbestpeakratios'] = best_peak_sampling_ratios
            pgram['siderealflags'] = close_to_sidereal_flag

    #
    # done with calculations, get the features we need
    #
    # get the best periods across all the period finding methods
    all_bestperiods = np.concatenate(
        [x['nbestperiods']
         for x in pgramlist if
         (x['method'] != 'win' and x['nbestperiods'] is not None)]
    )
    all_bestperiod_diffs = np.array(
        [abs(a-b) for a,b in combinations(all_bestperiods,2)]
    )

    all_sampling_ratios = np.concatenate(
        [x['nbestpeakratios']
         for x in pgramlist if
         (x['method'] != 'win' and x['nbestperiods'] is not None)]
    )

    all_sidereal_flags = np.concatenate(
        [x['siderealflags']
         for x in pgramlist if
         (x['method'] != 'win' and x['nbestperiods'] is not None)]
    )

    # bestperiods_n_abovesampling - number of top period estimates with peaks
    #                               that are at least sampling_peak_multiplier x
    #                               sampling peak height at the same period
    bestperiods_n_abovesampling = (
        all_sampling_ratios[all_sampling_ratios >
                            sampling_peak_multiplier]
    ).size
    # bestperiods_n_sidereal - number of top period estimates that are
    #                          consistent with a 1 day period (1.0027379 and
    #                          0.9972696 actually, for sidereal day period)
    bestperiods_n_sidereal = all_sidereal_flags.sum()

    # bestperiods_diffn_threshold - the number of cross-wise period diffs from
    #                               all period finders that fall below the
    #                               pdiff_threshold
    bestperiods_diffn_threshold = (
        all_bestperiod_diffs < pdiff_threshold
    ).size

    resdict = {
        'bestperiods_n_abovesampling':bestperiods_n_abovesampling,
        'bestperiods_n_sidereal':bestperiods_n_sidereal,
        'bestperiods_diffn_threshold':bestperiods_diffn_threshold
    }

    return resdict