def lightcurve_ptp_measures(ftimes, fmags, ferrs):
    '''This calculates various point-to-point measures (`eta` in Kim+ 2014).

    Parameters
    ----------

    ftimes,fmags,ferrs : np.array
        The input mag/flux time-series with all non-finite elements removed.

    Returns
    -------

    dict
        A dict with values of the point-to-point measures, including the `eta`
        variability index (often used as its inverse `inveta` to have the same
        sense as increasing variability index -> more likely a variable star).

    '''

    ndet = len(fmags)

    if ndet > 9:

        timediffs = npdiff(ftimes)

        # get rid of stuff with time diff = 0.0
        nzind = npnonzero(timediffs)
        ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

        # recalculate ndet and diffs
        ndet = ftimes.size
        timediffs = npdiff(ftimes)

        # calculate the point to point measures
        p2p_abs_magdiffs = npabs(npdiff(fmags))
        p2p_squared_magdiffs = npdiff(fmags)*npdiff(fmags)

        robstd = npmedian(npabs(fmags - npmedian(fmags)))*1.483
        robvar = robstd*robstd

        # these are eta from the Kim+ 2014 paper - ratio of point-to-point
        # difference to the variance of the entire series

        # this is the robust version
        eta_robust = npmedian(p2p_abs_magdiffs)/robvar
        eta_robust = eta_robust/(ndet - 1.0)

        # this is the usual version
        eta_normal = npsum(p2p_squared_magdiffs)/npvar(fmags)
        eta_normal = eta_normal/(ndet - 1.0)

        timeweights = 1.0/(timediffs*timediffs)

        # this is eta_e modified for uneven sampling from the Kim+ 2014 paper
        eta_uneven_normal = (
            (npsum(timeweights*p2p_squared_magdiffs) /
             (npvar(fmags) * npsum(timeweights)) ) *
            npmean(timeweights) *
            (ftimes.max() - ftimes.min())*(ftimes.max() - ftimes.min())
        )

        # this is robust eta_e modified for uneven sampling from the Kim+ 2014
        # paper
        eta_uneven_robust = (
            (npsum(timeweights*p2p_abs_magdiffs) /
             (robvar * npsum(timeweights)) ) *
            npmedian(timeweights) *
            (ftimes[-1] - ftimes[0])*(ftimes[-1] - ftimes[0])
        )

        return {
            'eta_normal':eta_normal,
            'eta_robust':eta_robust,
            'eta_uneven_normal':eta_uneven_normal,
            'eta_uneven_robust':eta_uneven_robust
        }

    else:

        return None