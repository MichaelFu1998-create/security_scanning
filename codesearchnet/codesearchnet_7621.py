def _kaiser(n, beta):
    """Independant Kaiser window

    For the definition of the Kaiser window, see A. V. Oppenheim & R. W. Schafer, "Discrete-Time Signal Processing".

    The continuous version of width n centered about x=0 is:

    .. note:: 2 times slower than scipy.kaiser
    """
    from scipy.special import iv as besselI
    m = n - 1
    k = arange(0, m)
    k = 2. * beta / m * sqrt (k * (m - k))
    w = besselI (0, k) / besselI (0, beta)
    return w