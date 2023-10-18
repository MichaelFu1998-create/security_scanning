def _epd_residual(coeffs, mags, fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd):
    '''
    This is the residual function to minimize using scipy.optimize.leastsq.

    '''

    f = _epd_function(coeffs, fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd)
    residual = mags - f
    return residual