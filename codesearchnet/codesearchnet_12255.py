def stetson_kindex(fmags, ferrs):
    '''This calculates the Stetson K index (a robust measure of the kurtosis).

    Parameters
    ----------

    fmags,ferrs : np.array
        The input mag/flux time-series to process. Must have no non-finite
        elems.

    Returns
    -------

    float
        The Stetson K variability index.

    '''

    # use a fill in value for the errors if they're none
    if ferrs is None:
        ferrs = npfull_like(fmags, 0.005)

    ndet = len(fmags)

    if ndet > 9:

        # get the median and ndet
        medmag = npmedian(fmags)

        # get the stetson index elements
        delta_prefactor = (ndet/(ndet - 1))
        sigma_i = delta_prefactor*(fmags - medmag)/ferrs

        stetsonk = (
            npsum(npabs(sigma_i))/(npsqrt(npsum(sigma_i*sigma_i))) *
            (ndet**(-0.5))
        )

        return stetsonk

    else:

        LOGERROR('not enough detections in this magseries '
                 'to calculate stetson K index')
        return npnan