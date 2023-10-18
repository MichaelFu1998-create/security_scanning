def sigclip_magseries(times, mags, errs,
                      sigclip=None,
                      iterative=False,
                      niterations=None,
                      meanormedian='median',
                      magsarefluxes=False):
    '''Sigma-clips a magnitude or flux time-series.

    Selects the finite times, magnitudes (or fluxes), and errors from the passed
    values, and apply symmetric or asymmetric sigma clipping to them.

    Parameters
    ----------

    times,mags,errs : np.array
        The magnitude or flux time-series arrays to sigma-clip. This doesn't
        assume all values are finite or if they're positive/negative. All of
        these arrays will have their non-finite elements removed, and then will
        be sigma-clipped based on the arguments to this function.

        `errs` is optional. Set it to None if you don't have values for these. A
        'faked' `errs` array will be generated if necessary, which can be
        ignored in the output as well.

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

    iterative : bool
        If this is set to True, will perform iterative sigma-clipping. If
        `niterations` is not set and this is True, sigma-clipping is iterated
        until no more points are removed.

    niterations : int
        The maximum number of iterations to perform for sigma-clipping. If None,
        the `iterative` arg takes precedence, and `iterative=True` will
        sigma-clip until no more points are removed.  If `niterations` is not
        None and `iterative` is False, `niterations` takes precedence and
        iteration will occur for the specified number of iterations.

    meanormedian : {'mean', 'median'}
        Use 'mean' for sigma-clipping based on the mean value, or 'median' for
        sigma-clipping based on the median value.  Default is 'median'.

    magsareflux : bool
        True if your "mags" are in fact fluxes, i.e. if "fainter" corresponds to
        `mags` getting smaller.

    Returns
    -------

    (stimes, smags, serrs) : tuple
        The sigma-clipped and nan-stripped time-series.

    '''

    returnerrs = True

    # fake the errors if they don't exist
    # this is inconsequential to sigma-clipping
    # we don't return these dummy values if the input errs are None
    if errs is None:
        # assume 0.1% errors if not given
        # this should work for mags and fluxes
        errs = 0.001*mags
        returnerrs = False

    # filter the input times, mags, errs; do sigclipping and normalization
    find = npisfinite(times) & npisfinite(mags) & npisfinite(errs)
    ftimes, fmags, ferrs = times[find], mags[find], errs[find]

    # get the center value and stdev
    if meanormedian == 'median':  # stddev = 1.483 x MAD

        center_mag = npmedian(fmags)
        stddev_mag = (npmedian(npabs(fmags - center_mag))) * 1.483

    elif meanormedian == 'mean':

        center_mag = npmean(fmags)
        stddev_mag = npstddev(fmags)

    else:
        LOGWARNING("unrecognized meanormedian value given to "
                   "sigclip_magseries: %s, defaulting to 'median'" %
                   meanormedian)
        meanormedian = 'median'
        center_mag = npmedian(fmags)
        stddev_mag = (npmedian(npabs(fmags - center_mag))) * 1.483

    # sigclip next for a single sigclip value
    if sigclip and isinstance(sigclip, (float, int)):

        if not iterative and niterations is None:

            sigind = (npabs(fmags - center_mag)) < (sigclip * stddev_mag)

            stimes = ftimes[sigind]
            smags = fmags[sigind]
            serrs = ferrs[sigind]

        else:

            #
            # iterative version adapted from scipy.stats.sigmaclip
            #

            # First, if niterations is not set, iterate until covergence
            if niterations is None:

                delta = 1

                this_times = ftimes
                this_mags = fmags
                this_errs = ferrs

                while delta:

                    if meanormedian == 'mean':
                        this_center = npmean(this_mags)
                        this_stdev = npstddev(this_mags)
                    elif meanormedian == 'median':
                        this_center = npmedian(this_mags)
                        this_stdev = (
                            npmedian(npabs(this_mags - this_center))
                        ) * 1.483
                    this_size = this_mags.size

                    # apply the sigclip
                    tsi = (
                        (npabs(this_mags - this_center)) <
                        (sigclip * this_stdev)
                    )

                    # update the arrays
                    this_times = this_times[tsi]
                    this_mags = this_mags[tsi]
                    this_errs = this_errs[tsi]

                    # update delta and go to the top of the loop
                    delta = this_size - this_mags.size

            else:  # If iterating only a certain number of times

                this_times = ftimes
                this_mags = fmags
                this_errs = ferrs

                iter_num = 0
                delta = 1
                while iter_num < niterations and delta:

                    if meanormedian == 'mean':

                        this_center = npmean(this_mags)
                        this_stdev = npstddev(this_mags)

                    elif meanormedian == 'median':

                        this_center = npmedian(this_mags)
                        this_stdev = (npmedian(npabs(this_mags -
                                                     this_center))) * 1.483
                    this_size = this_mags.size

                    # apply the sigclip
                    tsi = (
                        (npabs(this_mags - this_center)) <
                        (sigclip * this_stdev)
                    )

                    # update the arrays
                    this_times = this_times[tsi]
                    this_mags = this_mags[tsi]
                    this_errs = this_errs[tsi]

                    # update the number of iterations and delta and
                    # go to the top of the loop
                    delta = this_size - this_mags.size
                    iter_num += 1

            # final sigclipped versions
            stimes, smags, serrs = this_times, this_mags, this_errs


    # this handles sigclipping for asymmetric +ve and -ve clip values
    elif sigclip and isinstance(sigclip, (list,tuple)) and len(sigclip) == 2:

        # sigclip is passed as [dimmingclip, brighteningclip]
        dimmingclip = sigclip[0]
        brighteningclip = sigclip[1]

        if not iterative and niterations is None:

            if magsarefluxes:
                nottoodimind = (
                    (fmags - center_mag) > (-dimmingclip*stddev_mag)
                )
                nottoobrightind = (
                    (fmags - center_mag) < (brighteningclip*stddev_mag)
                )
            else:
                nottoodimind = (
                    (fmags - center_mag) < (dimmingclip*stddev_mag)
                )
                nottoobrightind = (
                    (fmags - center_mag) > (-brighteningclip*stddev_mag)
                )

            sigind = nottoodimind & nottoobrightind

            stimes = ftimes[sigind]
            smags = fmags[sigind]
            serrs = ferrs[sigind]

        else:

            #
            # iterative version adapted from scipy.stats.sigmaclip
            #
            if niterations is None:

                delta = 1

                this_times = ftimes
                this_mags = fmags
                this_errs = ferrs

                while delta:

                    if meanormedian == 'mean':

                        this_center = npmean(this_mags)
                        this_stdev = npstddev(this_mags)

                    elif meanormedian == 'median':
                        this_center = npmedian(this_mags)
                        this_stdev = (npmedian(npabs(this_mags -
                                                     this_center))) * 1.483
                    this_size = this_mags.size

                    if magsarefluxes:
                        nottoodimind = (
                            (this_mags - this_center) >
                            (-dimmingclip*this_stdev)
                        )
                        nottoobrightind = (
                            (this_mags - this_center) <
                            (brighteningclip*this_stdev)
                        )
                    else:
                        nottoodimind = (
                            (this_mags - this_center) <
                            (dimmingclip*this_stdev)
                        )
                        nottoobrightind = (
                            (this_mags - this_center) >
                            (-brighteningclip*this_stdev)
                        )

                    # apply the sigclip
                    tsi = nottoodimind & nottoobrightind

                    # update the arrays
                    this_times = this_times[tsi]
                    this_mags = this_mags[tsi]
                    this_errs = this_errs[tsi]

                    # update delta and go to top of the loop
                    delta = this_size - this_mags.size

            else:  # If iterating only a certain number of times
                this_times = ftimes
                this_mags = fmags
                this_errs = ferrs

                iter_num = 0
                delta = 1

                while iter_num < niterations and delta:

                    if meanormedian == 'mean':
                        this_center = npmean(this_mags)
                        this_stdev = npstddev(this_mags)
                    elif meanormedian == 'median':
                        this_center = npmedian(this_mags)
                        this_stdev = (npmedian(npabs(this_mags -
                                                     this_center))) * 1.483
                    this_size = this_mags.size

                    if magsarefluxes:
                        nottoodimind = (
                            (this_mags - this_center) >
                            (-dimmingclip*this_stdev)
                        )
                        nottoobrightind = (
                            (this_mags - this_center) <
                            (brighteningclip*this_stdev)
                        )
                    else:
                        nottoodimind = (
                            (this_mags - this_center) < (dimmingclip*this_stdev)
                        )
                        nottoobrightind = (
                            (this_mags - this_center) >
                            (-brighteningclip*this_stdev)
                        )

                    # apply the sigclip
                    tsi = nottoodimind & nottoobrightind

                    # update the arrays
                    this_times = this_times[tsi]
                    this_mags = this_mags[tsi]
                    this_errs = this_errs[tsi]

                    # update the number of iterations and delta
                    # and go to top of the loop
                    delta = this_size - this_mags.size
                    iter_num += 1

            # final sigclipped versions
            stimes, smags, serrs = this_times, this_mags, this_errs

    else:

        stimes = ftimes
        smags = fmags
        serrs = ferrs

    if returnerrs:
        return stimes, smags, serrs
    else:
        return stimes, smags, None