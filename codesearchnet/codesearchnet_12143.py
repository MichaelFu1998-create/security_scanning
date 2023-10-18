def _old_epd_magseries(times, mags, errs,
                       fsv, fdv, fkv, xcc, ycc, bgv, bge,
                       epdsmooth_windowsize=21,
                       epdsmooth_sigclip=3.0,
                       epdsmooth_func=smooth_magseries_signal_medfilt,
                       epdsmooth_extraparams=None):
    '''
    Detrends a magnitude series given in mag using accompanying values of S in
    fsv, D in fdv, K in fkv, x coords in xcc, y coords in ycc, background in
    bgv, and background error in bge. smooth is used to set a smoothing
    parameter for the fit function. Does EPD voodoo.

    '''

    # find all the finite values of the magsnitude
    finiteind = np.isfinite(mags)

    # calculate median and stdev
    mags_median = np.median(mags[finiteind])
    mags_stdev = np.nanstd(mags)

    # if we're supposed to sigma clip, do so
    if epdsmooth_sigclip:
        excludeind = abs(mags - mags_median) < epdsmooth_sigclip*mags_stdev
        finalind = finiteind & excludeind
    else:
        finalind = finiteind

    final_mags = mags[finalind]
    final_len = len(final_mags)

    # smooth the signal
    if isinstance(epdsmooth_extraparams, dict):
        smoothedmags = epdsmooth_func(final_mags,
                                      epdsmooth_windowsize,
                                      **epdsmooth_extraparams)
    else:
        smoothedmags = epdsmooth_func(final_mags, epdsmooth_windowsize)

    # make the linear equation matrix
    epdmatrix = np.c_[fsv[finalind]**2.0,
                      fsv[finalind],
                      fdv[finalind]**2.0,
                      fdv[finalind],
                      fkv[finalind]**2.0,
                      fkv[finalind],
                      np.ones(final_len),
                      fsv[finalind]*fdv[finalind],
                      fsv[finalind]*fkv[finalind],
                      fdv[finalind]*fkv[finalind],
                      np.sin(2*np.pi*xcc[finalind]),
                      np.cos(2*np.pi*xcc[finalind]),
                      np.sin(2*np.pi*ycc[finalind]),
                      np.cos(2*np.pi*ycc[finalind]),
                      np.sin(4*np.pi*xcc[finalind]),
                      np.cos(4*np.pi*xcc[finalind]),
                      np.sin(4*np.pi*ycc[finalind]),
                      np.cos(4*np.pi*ycc[finalind]),
                      bgv[finalind],
                      bge[finalind]]

    # solve the matrix equation [epdmatrix] . [x] = [smoothedmags]
    # return the EPD differential magss if the solution succeeds
    try:

        coeffs, residuals, rank, singulars = lstsq(epdmatrix, smoothedmags,
                                                   rcond=None)

        if DEBUG:
            print('coeffs = %s, residuals = %s' % (coeffs, residuals))


        retdict = {'times':times,
                   'mags':(mags_median +
                           _old_epd_diffmags(coeffs, fsv, fdv,
                                             fkv, xcc, ycc, bgv, bge, mags)),
                   'errs':errs,
                   'fitcoeffs':coeffs,
                   'residuals':residuals}

        return retdict

    # if the solution fails, return nothing
    except Exception as e:

        LOGEXCEPTION('EPD solution did not converge')

        retdict = {'times':times,
                   'mags':np.full_like(mags, np.nan),
                   'errs':errs,
                   'fitcoeffs':coeffs,
                   'residuals':residuals}

        return retdict