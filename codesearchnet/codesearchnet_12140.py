def smooth_magseries_gaussfilt(mags, windowsize, windowfwhm=7):
    '''This smooths the magseries with a Gaussian kernel.

    Parameters
    ----------

    mags : np.array
        The input mags/flux time-series to smooth.

    windowsize : int
        This is a odd integer containing the smoothing window size.

    windowfwhm : int
        This is an odd integer containing the FWHM of the applied Gaussian
        window function.

    Returns
    -------

    np.array
        The smoothed mag/flux time-series array.

    '''

    convkernel = Gaussian1DKernel(windowfwhm, x_size=windowsize)
    smoothed = convolve(mags, convkernel, boundary='extend')
    return smoothed