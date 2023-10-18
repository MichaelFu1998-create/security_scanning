def all_nonperiodic_features(times, mags, errs,
                             magsarefluxes=False,
                             stetson_weightbytimediff=True):
    '''This rolls up the feature functions above and returns a single dict.

    NOTE: this doesn't calculate the CDPP to save time since binning and
    smoothing takes a while for dense light curves.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to calculate CDPP for.

    magsarefluxes : bool
        If True, indicates `mags` is actually an array of flux values.

    stetson_weightbytimediff : bool
        If this is True, the Stetson index for any pair of mags will be
        reweighted by the difference in times between them using the scheme in
        Fruth+ 2012 and Zhange+ 2003 (as seen in Sokolovsky+ 2017)::

            w_i = exp(- (t_i+1 - t_i)/ delta_t )

    Returns
    -------

    dict
        Returns a dict with all of the variability features.

    '''

    # remove nans first
    finiteind = npisfinite(times) & npisfinite(mags) & npisfinite(errs)
    ftimes, fmags, ferrs = times[finiteind], mags[finiteind], errs[finiteind]

    # remove zero errors
    nzind = npnonzero(ferrs)
    ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

    xfeatures = nonperiodic_lightcurve_features(times, mags, errs,
                                                magsarefluxes=magsarefluxes)
    stetj = stetson_jindex(ftimes, fmags, ferrs,
                           weightbytimediff=stetson_weightbytimediff)
    stetk = stetson_kindex(fmags, ferrs)

    xfeatures.update({'stetsonj':stetj,
                      'stetsonk':stetk})

    return xfeatures