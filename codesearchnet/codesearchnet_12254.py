def stetson_jindex(ftimes, fmags, ferrs, weightbytimediff=False):
    '''This calculates the Stetson index for the magseries, based on consecutive
    pairs of observations.

    Based on Nicole Loncke's work for her Planets and Life certificate at
    Princeton in 2014.

    Parameters
    ----------

    ftimes,fmags,ferrs : np.array
        The input mag/flux time-series with all non-finite elements removed.

    weightbytimediff : bool
        If this is True, the Stetson index for any pair of mags will be
        reweighted by the difference in times between them using the scheme in
        Fruth+ 2012 and Zhange+ 2003 (as seen in Sokolovsky+ 2017)::

            w_i = exp(- (t_i+1 - t_i)/ delta_t )

    Returns
    -------

    float
        The calculated Stetson J variability index.

    '''

    ndet = len(fmags)

    if ndet > 9:

        # get the median and ndet
        medmag = npmedian(fmags)

        # get the stetson index elements
        delta_prefactor = (ndet/(ndet - 1))
        sigma_i = delta_prefactor*(fmags - medmag)/ferrs

        # Nicole's clever trick to advance indices by 1 and do x_i*x_(i+1)
        sigma_j = nproll(sigma_i,1)

        if weightbytimediff:

            difft = npdiff(ftimes)
            deltat = npmedian(difft)

            weights_i = npexp(- difft/deltat )
            products = (weights_i*sigma_i[1:]*sigma_j[1:])
        else:
            # ignore first elem since it's actually x_0*x_n
            products = (sigma_i*sigma_j)[1:]

        stetsonj = (
            npsum(npsign(products) * npsqrt(npabs(products)))
        ) / ndet

        return stetsonj

    else:

        LOGERROR('not enough detections in this magseries '
                 'to calculate stetson J index')
        return npnan