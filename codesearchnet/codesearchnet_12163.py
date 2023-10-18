def _epd_function(coeffs, fluxes, xcc, ycc, bgv, bge):
    '''This is the EPD function to fit.

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
        Contains the fit function evaluated at each flux measurement value.

    '''

    epdf = (
        coeffs[0] +
        coeffs[1]*npsin(2*MPI*xcc) + coeffs[2]*npcos(2*MPI*xcc) +
        coeffs[3]*npsin(2*MPI*ycc) + coeffs[4]*npcos(2*MPI*ycc) +
        coeffs[5]*npsin(4*MPI*xcc) + coeffs[6]*npcos(4*MPI*xcc) +
        coeffs[7]*npsin(4*MPI*ycc) + coeffs[8]*npcos(4*MPI*ycc) +
        coeffs[9]*bgv +
        coeffs[10]*bge
    )

    return epdf