def gaussian(x, mu, sigma):
    """
    Gaussian function of the form :math:`\\frac{1}{\\sqrt{2 \\pi}\\sigma} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}`.

    .. versionadded:: 1.5

    Parameters
    ----------
    x : float
        Function variable :math:`x`.
    mu : float
        Mean of the Gaussian function.
    sigma : float
        Standard deviation of the Gaussian function.
    """
    return _np.exp(-(x-mu)**2/(2*sigma**2)) / (_np.sqrt(2*_np.pi) * sigma)