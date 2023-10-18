def sigma2fwhm(sigma):
    """Convert a sigma in a Gaussian kernel to a FWHM value.

    Parameters
    ----------
    sigma: float or numpy.array
       sigma value or values

    Returns
    -------
    fwhm: float or numpy.array
       fwhm values corresponding to `sigma` values
    """
    sigma = np.asarray(sigma)
    return np.sqrt(8 * np.log(2)) * sigma