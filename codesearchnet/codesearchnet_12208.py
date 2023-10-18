def _fourier_chisq(fourierparams,
                   phase,
                   mags,
                   errs):
    '''This is the chisq objective function to be minimized by `scipy.minimize`.

    The parameters are the same as `_fourier_func` above. `errs` is used to
    calculate the chisq value.

    '''

    f = _fourier_func(fourierparams, phase, mags)
    chisq = npsum(((mags - f)*(mags - f))/(errs*errs))

    return chisq