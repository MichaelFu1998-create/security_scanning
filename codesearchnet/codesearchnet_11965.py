def normalize_magseries(times,
                        mags,
                        mingap=4.0,
                        normto='globalmedian',
                        magsarefluxes=False,
                        debugmode=False):
    '''This normalizes the magnitude time-series to a specified value.

    This is used to normalize time series measurements that may have large time
    gaps and vertical offsets in mag/flux measurement between these
    'timegroups', either due to instrument changes or different filters.

    NOTE: this works in-place! The mags array will be replaced with normalized
    mags when this function finishes.

    Parameters
    ----------

    times,mags : array-like
        The times (assumed to be some form of JD) and mags (or flux)
        measurements to be normalized.

    mingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    normto : {'globalmedian', 'zero'} or a float
        Specifies the normalization type::

          'globalmedian' -> norms each mag to the global median of the LC column
          'zero'         -> norms each mag to zero
          a float        -> norms each mag to this specified float value.

    magsarefluxes : bool
        Indicates if the input `mags` array is actually an array of flux
        measurements instead of magnitude measurements. If this is set to True,
        then:

        - if `normto` is 'zero', then the median flux is divided from each
          observation's flux value to yield normalized fluxes with 1.0 as the
          global median.

        - if `normto` is 'globalmedian', then the global median flux value
          across the entire time series is multiplied with each measurement.

        - if `norm` is set to a `float`, then this number is multiplied with the
          flux value for each measurement.

    debugmode : bool
        If this is True, will print out verbose info on each timegroup found.

    Returns
    -------

    times,normalized_mags : np.arrays
        Normalized magnitude values after normalization. If normalization fails
        for some reason, `times` and `normalized_mags` will both be None.

    '''

    ngroups, timegroups = find_lc_timegroups(times,
                                             mingap=mingap)

    # find all the non-nan indices
    finite_ind = np.isfinite(mags)

    if any(finite_ind):

        # find the global median
        global_mag_median = np.median(mags[finite_ind])

        # go through the groups and normalize them to the median for
        # each group
        for tgind, tg in enumerate(timegroups):

            finite_ind = np.isfinite(mags[tg])

            # find this timegroup's median mag and normalize the mags in
            # it to this median
            group_median = np.median((mags[tg])[finite_ind])

            if magsarefluxes:
                mags[tg] = mags[tg]/group_median
            else:
                mags[tg] = mags[tg] - group_median

            if debugmode:
                LOGDEBUG('group %s: elems %s, '
                         'finite elems %s, median mag %s' %
                         (tgind,
                          len(mags[tg]),
                          len(finite_ind),
                          group_median))

        # now that everything is normalized to 0.0, add the global median
        # offset back to all the mags and write the result back to the dict
        if isinstance(normto, str) and normto == 'globalmedian':

            if magsarefluxes:
                mags = mags * global_mag_median
            else:
                mags = mags + global_mag_median

        # if the normto is a float, add everything to that float and return
        elif isinstance(normto, float):

            if magsarefluxes:
                mags = mags * normto
            else:
                mags = mags + normto

        # anything else just returns the normalized mags as usual
        return times, mags

    else:
        LOGERROR('measurements are all nan!')
        return None, None