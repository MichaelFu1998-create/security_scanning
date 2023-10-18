def specwindow_lsp_value(times, mags, errs, omega):
    '''This calculates the peak associated with the spectral window function
    for times and at the specified omega.

    NOTE: this is classical Lomb-Scargle, not the Generalized
    Lomb-Scargle. `mags` and `errs` are silently ignored since we're calculating
    the periodogram of the observing window function. These are kept to present
    a consistent external API so the `pgen_lsp` function below can call this
    transparently.

    Parameters
    ----------

    times,mags,errs : np.array
        The time-series to calculate the periodogram value for.

    omega : float
        The frequency to calculate the periodogram value at.

    Returns
    -------

    periodogramvalue : float
        The normalized periodogram at the specified test frequency `omega`.

    '''

    norm_times = times - times.min()

    tau = (
        (1.0/(2.0*omega)) *
        nparctan( npsum(npsin(2.0*omega*norm_times)) /
                  npsum(npcos(2.0*omega*norm_times)) )
    )

    lspval_top_cos = (npsum(1.0 * npcos(omega*(norm_times-tau))) *
                      npsum(1.0 * npcos(omega*(norm_times-tau))))
    lspval_bot_cos = npsum( (npcos(omega*(norm_times-tau))) *
                            (npcos(omega*(norm_times-tau))) )

    lspval_top_sin = (npsum(1.0 * npsin(omega*(norm_times-tau))) *
                      npsum(1.0 * npsin(omega*(norm_times-tau))))
    lspval_bot_sin = npsum( (npsin(omega*(norm_times-tau))) *
                            (npsin(omega*(norm_times-tau))) )

    lspval = 0.5 * ( (lspval_top_cos/lspval_bot_cos) +
                     (lspval_top_sin/lspval_bot_sin) )

    return lspval