def phasedlc_features(times,
                      mags,
                      errs,
                      period,
                      nbrtimes=None,
                      nbrmags=None,
                      nbrerrs=None):
    '''This calculates various phased LC features for the object.

    Some of the features calculated here come from:

    Kim, D.-W., Protopapas, P., Bailer-Jones, C. A. L., et al. 2014, Astronomy
    and Astrophysics, 566, A43, and references therein (especially Richards, et
    al. 2011).

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to calculate the phased LC features for.

    period : float
        The period used to phase the input mag/flux time-series.

    nbrtimes,nbrmags,nbrerrs : np.array or None
        If `nbrtimes`, `nbrmags`, and `nbrerrs` are all provided, they should be
        ndarrays with `times`, `mags`, `errs` of this object's closest neighbor
        (close within some small number x FWHM of telescope to check for
        blending). This function will then also calculate extra features based
        on the neighbor's phased LC using the `period` provided for the target
        object.

    Returns
    -------

    dict
        Returns a dict with phased LC features.

    '''
    # get the finite values
    finind = np.isfinite(times) & np.isfinite(mags) & np.isfinite(errs)
    ftimes, fmags, ferrs = times[finind], mags[finind], errs[finind]

    # get nonzero errors
    nzind = np.nonzero(ferrs)
    ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

    # only operate on LC if enough points
    if ftimes.size > 49:

        # get the MAD of the unphased light curve
        lightcurve_median = np.median(fmags)
        lightcurve_mad = np.median(np.abs(fmags - lightcurve_median))

        # get p2p for raw lightcurve
        p2p_unphasedlc = lightcurve_ptp_measures(ftimes, fmags, ferrs)
        inveta_unphasedlc = 1.0/p2p_unphasedlc['eta_normal']

        # phase the light curve with the given period, assume epoch is
        # times.min()
        phasedlc = lcmath.phase_magseries_with_errs(ftimes, fmags, ferrs,
                                                    period, ftimes.min(),
                                                    wrap=False)

        phase = phasedlc['phase']
        pmags = phasedlc['mags']
        perrs = phasedlc['errs']

        # get ptp measures for best period
        ptp_bestperiod = lightcurve_ptp_measures(phase,pmags,perrs)

        # phase the light curve with the given periodx2, assume epoch is
        # times.min()
        phasedlc = lcmath.phase_magseries_with_errs(ftimes, fmags, ferrs,
                                                    period*2.0, ftimes.min(),
                                                    wrap=False)

        phasex2 = phasedlc['phase']
        pmagsx2 = phasedlc['mags']
        perrsx2 = phasedlc['errs']


        # get ptp measures for best periodx2
        ptp_bestperiodx2 = lightcurve_ptp_measures(phasex2,pmagsx2,perrsx2)

        # eta_phasedlc_bestperiod - calculate eta for the phased LC with best
        # period
        inveta_bestperiod = 1.0/ptp_bestperiod['eta_normal']

        # eta_phasedlc_bestperiodx2 - calculate eta for the phased LC with best
        #                             period x 2
        inveta_bestperiodx2 = 1.0/ptp_bestperiodx2['eta_normal']


        # eta_phased_ratio_eta_raw - eta for best period phased LC / eta for raw
        # LC
        inveta_ratio_phased_unphased = inveta_bestperiod/inveta_unphasedlc

        # eta_phasedx2_ratio_eta_raw - eta for best periodx2 phased LC/eta for
        # raw LC
        inveta_ratio_phasedx2_unphased = inveta_bestperiodx2/inveta_unphasedlc


        # freq_model_max_delta_mags - absval of magdiff btw model phased LC
        #                             maxima using period x 2. look at points
        #                             more than 10 points away for maxima
        phasedx2_maxval_ind = argrelmax(pmagsx2, order=10)
        if phasedx2_maxval_ind[0].size > 1:
            phasedx2_magdiff_maxval = (
                np.max(np.abs(np.diff(pmagsx2[phasedx2_maxval_ind[0]])))
            )
        else:
            phasedx2_magdiff_maxval = np.nan

        # freq_model_min_delta_mags - absval of magdiff btw model phased LC
        #                             minima using period x 2. look at points
        #                             more than 10 points away for minima
        phasedx2_minval_ind = argrelmin(pmagsx2, order=10)
        if phasedx2_minval_ind[0].size > 1:
            phasedx2_magdiff_minval = (
                np.max(np.abs(np.diff(pmagsx2[phasedx2_minval_ind[0]])))
            )
        else:
            phasedx2_magdiff_minval = np.nan

        # p2p_scatter_pfold_over_mad - MAD of successive absolute mag diffs of
        #                              the phased LC using best period divided
        #                              by the MAD of the unphased LC
        phased_magdiff = np.diff(pmags)
        phased_magdiff_median = np.median(phased_magdiff)
        phased_magdiff_mad = np.median(np.abs(phased_magdiff -
                                              phased_magdiff_median))

        phasedx2_magdiff = np.diff(pmagsx2)
        phasedx2_magdiff_median = np.median(phasedx2_magdiff)
        phasedx2_magdiff_mad = np.median(np.abs(phasedx2_magdiff -
                                                phasedx2_magdiff_median))

        phased_magdiffmad_unphased_mad_ratio = phased_magdiff_mad/lightcurve_mad
        phasedx2_magdiffmad_unphased_mad_ratio = (
            phasedx2_magdiff_mad/lightcurve_mad
        )

        # get the percentiles of the slopes of the adjacent mags for phasedx2
        phasedx2_slopes = np.diff(pmagsx2)/np.diff(phasex2)
        phasedx2_slope_percentiles = np.ravel(np.nanpercentile(phasedx2_slopes,
                                                               [10.0,90.0]))
        phasedx2_slope_10percentile = phasedx2_slope_percentiles[0]
        phasedx2_slope_90percentile = phasedx2_slope_percentiles[1]

        # check if nbrtimes, _mags, _errs are available
        if ((nbrtimes is not None) and
            (nbrmags is not None) and
            (nbrerrs is not None)):

            # get the finite values
            nfinind = (np.isfinite(nbrtimes) &
                       np.isfinite(nbrmags) &
                       np.isfinite(nbrerrs))
            nftimes, nfmags, nferrs = (nbrtimes[nfinind],
                                       nbrmags[nfinind],
                                       nbrerrs[nfinind])

            # get nonzero errors
            nnzind = np.nonzero(nferrs)
            nftimes, nfmags, nferrs = (nftimes[nnzind],
                                       nfmags[nnzind],
                                       nferrs[nnzind])

            # only operate on LC if enough points
            if nftimes.size > 49:

                # get the phased light curve using the same period and epoch as
                # the actual object
                nphasedlc = lcmath.phase_magseries_with_errs(
                    nftimes, nfmags, nferrs,
                    period, ftimes.min(),
                    wrap=False
                )

                # normalize the object and neighbor phased mags
                norm_pmags = pmags - np.median(pmags)
                norm_npmags = nphasedlc['mags'] - np.median(nphasedlc['mags'])

                # phase bin them both so we can compare LCs easily
                phabinned_objectlc = lcmath.phase_bin_magseries(phase,
                                                                norm_pmags,
                                                                minbinelems=1)
                phabinned_nbrlc = lcmath.phase_bin_magseries(nphasedlc['phase'],
                                                             norm_npmags,
                                                             minbinelems=1)

                absdiffs = []

                for pha, phamag in zip(phabinned_objectlc['binnedphases'],
                                       phabinned_objectlc['binnedmags']):

                    try:

                        # get the matching phase from the neighbor phased LC
                        phadiffs = np.abs(pha - phabinned_nbrlc['binnedphases'])
                        minphadiffind = np.where(
                            (phadiffs < 1.0e-4) &
                            (phadiffs == np.min(phadiffs))
                        )
                        absmagdiff = np.abs(
                            phamag - phabinned_nbrlc['binnedmags'][
                                minphadiffind
                            ]
                        )
                        if absmagdiff.size > 0:
                            absdiffs.append(absmagdiff.min())

                    except Exception as e:
                        continue

                # sum of absdiff between the normalized to 0.0 phased LC of this
                # object and that of the closest neighbor phased with the same
                # period and epoch
                if len(absdiffs) > 0:
                    sum_nbr_phasedlc_magdiff = sum(absdiffs)
                else:
                    sum_nbr_phasedlc_magdiff = np.nan

            else:

                sum_nbr_phasedlc_magdiff = np.nan

        else:
            sum_nbr_phasedlc_magdiff = np.nan

        return {
            'inveta_unphasedlc':inveta_unphasedlc,
            'inveta_bestperiod':inveta_bestperiod,
            'inveta_bestperiodx2':inveta_bestperiodx2,
            'inveta_ratio_phased_unphased':inveta_ratio_phased_unphased,
            'inveta_ratio_phasedx2_unphased':inveta_ratio_phasedx2_unphased,
            'phasedx2_magdiff_maxima':phasedx2_magdiff_maxval,
            'phasedx2_magdiff_minina':phasedx2_magdiff_minval,
            'phased_unphased_magdiff_mad_ratio':(
                phased_magdiffmad_unphased_mad_ratio
            ),
            'phasedx2_unphased_magdiff_mad_ratio':(
                phasedx2_magdiffmad_unphased_mad_ratio
            ),
            'phasedx2_slope_10percentile':phasedx2_slope_10percentile,
            'phasedx2_slope_90percentile':phasedx2_slope_90percentile,
            'sum_nbr_phasedlc_magdiff':sum_nbr_phasedlc_magdiff,
        }

    else:

        return {
            'inveta_unphasedlc':np.nan,
            'inveta_bestperiod':np.nan,
            'inveta_bestperiodx2':np.nan,
            'inveta_ratio_phased_unphased':np.nan,
            'inveta_ratio_phasedx2_unphased':np.nan,
            'phasedx2_magdiff_maxima':np.nan,
            'phasedx2_magdiff_minina':np.nan,
            'phased_unphased_magdiff_mad_ratio':np.nan,
            'phasedx2_unphased_magdiff_mad_ratio':np.nan,
            'phasedx2_slope_10percentile':np.nan,
            'phasedx2_slope_90percentile':np.nan,
            'sum_nbr_phasedlc_magdiff':np.nan,
        }