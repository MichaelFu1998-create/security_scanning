def _fourier_residual(fourierparams,
                      phase,
                      mags):
    '''
    This is the residual objective function to be minimized by `scipy.leastsq`.

    The parameters are the same as `_fourier_func` above.

    '''

    f = _fourier_func(fourierparams, phase, mags)
    residual = mags - f

    return residual