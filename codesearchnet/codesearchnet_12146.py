def _epd_residual2(coeffs,
                   times, mags, errs,
                   fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd):
    '''This is the residual function to minimize using
    scipy.optimize.least_squares.

    This variant is for :py:func:`.epd_magseries_extparams`.

    '''

    f = _epd_function(coeffs, fsv, fdv, fkv, xcc, ycc, bgv, bge, iha, izd)
    residual = mags - f
    return residual