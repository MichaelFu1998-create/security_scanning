def _epd_residual(coeffs, fluxes, xcc, ycc, bgv, bge):
    '''This is the residual function to minimize using scipy.optimize.leastsq.

    Parameters
    ----------

    coeffs : array-like of floats
        Contains the EPD coefficients that will be used to generate the EPD fit
        function.

    fluxes : array-like
        The flux measurement array being used.

    xcc,ycc : array-like
        Arrays of the x and y coordinates associated with each measurement in
        `fluxes`.

    bgv,bge : array-like
        Arrays of the flux background value and the flux background error
        associated with each measurement in `fluxes`.

    Returns
    -------

    np.array
        Contains the fit function residual evaluated at each flux measurement
        value.

    '''

    f = _epd_function(coeffs, fluxes, xcc, ycc, bgv, bge)
    residual = fluxes - f
    return residual