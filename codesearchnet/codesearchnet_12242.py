def specwindow_lsp(
        times,
        mags,
        errs,
        magsarefluxes=False,
        startp=None,
        endp=None,
        stepsize=1.0e-4,
        autofreq=True,
        nbestpeaks=5,
        periodepsilon=0.1,
        sigclip=10.0,
        nworkers=None,
        glspfunc=_glsp_worker_specwindow,
        verbose=True
):
    '''This calculates the spectral window function.

    Wraps the `pgen_lsp` function above to use the specific worker for
    calculating the window-function.

    Parameters
    ----------

    times,mags,errs : np.array
        The mag/flux time-series with associated measurement errors to run the
        period-finding on.

    magsarefluxes : bool
        If the input measurement values in `mags` and `errs` are in fluxes, set
        this to True.

    startp,endp : float or None
        The minimum and maximum periods to consider for the transit search.

    stepsize : float
        The step-size in frequency to use when constructing a frequency grid for
        the period search.

    autofreq : bool
        If this is True, the value of `stepsize` will be ignored and the
        :py:func:`astrobase.periodbase.get_frequency_grid` function will be used
        to generate a frequency grid based on `startp`, and `endp`. If these are
        None as well, `startp` will be set to 0.1 and `endp` will be set to
        `times.max() - times.min()`.

    nbestpeaks : int
        The number of 'best' peaks to return from the periodogram results,
        starting from the global maximum of the periodogram peak values.

    periodepsilon : float
        The fractional difference between successive values of 'best' periods
        when sorting by periodogram power to consider them as separate periods
        (as opposed to part of the same periodogram peak). This is used to avoid
        broad peaks in the periodogram and make sure the 'best' periods returned
        are all actually independent.

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

    nworkers : int
        The number of parallel workers to use when calculating the periodogram.

    glspfunc : Python function
        The worker function to use to calculate the periodogram. This is used to
        used to make the `pgen_lsp` function calculate the time-series sampling
        window function instead of the time-series measurements' GLS periodogram
        by passing in `_glsp_worker_specwindow` instead of the default
        `_glsp_worker` function.

    verbose : bool
        If this is True, will indicate progress and details about the frequency
        grid used for the period search.

    Returns
    -------

    dict
        This function returns a dict, referred to as an `lspinfo` dict in other
        astrobase functions that operate on periodogram results. This is a
        standardized format across all astrobase period-finders, and is of the
        form below::

            {'bestperiod': the best period value in the periodogram,
             'bestlspval': the periodogram peak associated with the best period,
             'nbestpeaks': the input value of nbestpeaks,
             'nbestlspvals': nbestpeaks-size list of best period peak values,
             'nbestperiods': nbestpeaks-size list of best periods,
             'lspvals': the full array of periodogram powers,
             'periods': the full array of periods considered,
             'method':'win' -> the name of the period-finder method,
             'kwargs':{ dict of all of the input kwargs for record-keeping}}

    '''

    # run the LSP using glsp_worker_specwindow as the worker
    lspres = pgen_lsp(
        times,
        mags,
        errs,
        magsarefluxes=magsarefluxes,
        startp=startp,
        endp=endp,
        autofreq=autofreq,
        nbestpeaks=nbestpeaks,
        periodepsilon=periodepsilon,
        stepsize=stepsize,
        nworkers=nworkers,
        sigclip=sigclip,
        glspfunc=glspfunc,
        verbose=verbose
    )

    # update the resultdict to indicate we're a spectral window function
    lspres['method'] = 'win'

    if lspres['lspvals'] is not None:

        # renormalize the periodogram to between 0 and 1 like the usual GLS.
        lspmax = npnanmax(lspres['lspvals'])

        if npisfinite(lspmax):

            lspres['lspvals'] = lspres['lspvals']/lspmax
            lspres['nbestlspvals'] = [
                x/lspmax for x in lspres['nbestlspvals']
            ]
            lspres['bestlspval'] = lspres['bestlspval']/lspmax

    return lspres