def enbw(data):
    r"""Computes the equivalent noise bandwidth

    .. math:: ENBW = N \frac{\sum_{n=1}^{N} w_n^2}{\left(\sum_{n=1}^{N} w_n \right)^2}

    .. doctest::

        >>> from spectrum import create_window, enbw
        >>> w = create_window(64, 'rectangular')
        >>> enbw(w)
        1.0

    The following table contains the ENBW values for some of the
    implemented windows in this module (with N=16384). They have been
    double checked against litterature (Source: [Harris]_, [Marple]_).

    If not present, it means that it has not been checked.

    =================== ============ =============
    name                 ENBW        litterature
    =================== ============ =============
    rectangular         1.           1.
    triangle            1.3334       1.33
    Hann                1.5001       1.5
    Hamming             1.3629       1.36
    blackman            1.7268       1.73
    kaiser              1.7
    blackmanharris,4    2.004        2.
    riesz               1.2000       1.2
    riemann             1.32         1.3
    parzen              1.917        1.92
    tukey 0.25          1.102        1.1
    bohman              1.7858       1.79
    poisson 2           1.3130       1.3
    hanningpoisson 0.5  1.609        1.61
    cauchy              1.489        1.48
    lanczos             1.3
    =================== ============ =============


    """
    N = len(data)
    return N * np.sum(data**2) / np.sum(data)**2