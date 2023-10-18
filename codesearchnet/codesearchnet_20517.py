def fwhm2sigma(fwhm):
    """Convert a FWHM value to sigma in a Gaussian kernel.

    Parameters
    ----------
    fwhm: float or numpy.array
       fwhm value or values

    Returns
    -------
    fwhm: float or numpy.array
       sigma values
    """
    fwhm = np.asarray(fwhm)
    return fwhm / np.sqrt(8 * np.log(2))