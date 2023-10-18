def get_epochs_given_midtimes_and_period(
        t_mid,
        period,
        err_t_mid=None,
        t0_fixed=None,
        t0_percentile=None,
        verbose=False
):
    '''This calculates the future epochs for a transit, given a period and a
    starting epoch

    The equation used is::

        t_mid = period*epoch + t0

    Default behavior if no kwargs are used is to define `t0` as the median
    finite time of the passed `t_mid` array.

    Only one of `err_t_mid` or `t0_fixed` should be passed.

    Parameters
    ----------

    t_mid : np.array
        A np.array of transit mid-time measurements

    period : float
        The period used to calculate epochs, per the equation above. For typical
        use cases, a period precise to ~1e-5 days is sufficient to get correct
        epochs.

    err_t_mid : None or np.array
        If provided, contains the errors of the transit mid-time
        measurements. The zero-point epoch is then set equal to the average of
        the transit times, weighted as `1/err_t_mid^2` . This minimizes the
        covariance between the transit epoch and the period (e.g., Gibson et
        al. 2013). For standard O-C analysis this is the best method.

    t0_fixed : None or float:
        If provided, use this t0 as the starting epoch. (Overrides all others).

    t0_percentile : None or float
        If provided, use this percentile of `t_mid` to define `t0`.

    Returns
    -------

    tuple
        This is the of the form `(integer_epoch_array, t0)`.
        `integer_epoch_array` is an array of integer epochs (float-type),
        of length equal to the number of *finite* mid-times passed.

    '''

    kwargarr = np.array([isinstance(err_t_mid,np.ndarray),
                         t0_fixed,
                         t0_percentile])
    if not _single_true(kwargarr) and not np.all(~kwargarr.astype(bool)):
        raise AssertionError(
            'can have at most one of err_t_mid, t0_fixed, t0_percentile')

    t_mid = t_mid[np.isfinite(t_mid)]
    N_midtimes = len(t_mid)

    if t0_fixed:
        t0 = t0_fixed
    elif isinstance(err_t_mid,np.ndarray):
        # get the weighted average. then round it to the nearest transit epoch.
        t0_avg = np.average(t_mid, weights=1/err_t_mid**2)
        t0_options = np.arange(min(t_mid), max(t_mid)+period, period)
        t0 = t0_options[np.argmin(np.abs(t0_options - t0_avg))]
    else:
        if not t0_percentile:
            # if there are an odd number of times, take the median time as
            # epoch=0.  elif there are an even number of times, take the lower
            # of the two middle times as epoch=0.
            if N_midtimes % 2 == 1:
                t0 = np.median(t_mid)
            else:
                t0 = t_mid[int(N_midtimes/2)]
        else:
            t0 = np.sort(t_mid)[int(N_midtimes*t0_percentile/100)]

    epoch = (t_mid - t0)/period

    # do not convert numpy entries to actual ints, because np.nan is float type
    int_epoch = np.round(epoch, 0)

    if verbose:
        LOGINFO('epochs before rounding')
        LOGINFO('\n{:s}'.format(repr(epoch)))
        LOGINFO('epochs after rounding')
        LOGINFO('\n{:s}'.format(repr(int_epoch)))

    return int_epoch, t0