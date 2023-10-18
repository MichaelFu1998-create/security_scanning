def _smooth_acf(acf, windowfwhm=7, windowsize=21):
    '''This returns a smoothed version of the ACF.

    Convolves the ACF with a Gaussian of given `windowsize` and `windowfwhm`.

    Parameters
    ----------

    acf : np.array
        The auto-correlation function array to smooth.

    windowfwhm : int
        The smoothing window Gaussian kernel's FWHM .

    windowsize : int
        The number of input points to apply the smoothing over.

    Returns
    -------

    np.array
        Smoothed version of the input ACF array.

    '''

    convkernel = Gaussian1DKernel(windowfwhm, x_size=windowsize)
    smoothed = convolve(acf, convkernel, boundary='extend')

    return smoothed