def tf2zpk(b, a):
    """Return zero, pole, gain (z,p,k) representation from a numerator,
    denominator representation of a linear filter.

    Convert zero-pole-gain filter parameters to transfer function form

    :param ndarray b:  numerator polynomial.
    :param ndarray a: numerator and denominator polynomials.

    :return:
        * z : ndarray        Zeros of the transfer function.
        * p : ndarray        Poles of the transfer function.
        * k : float        System gain.

    If some values of b are too close to 0, they are removed. In that case, a
    BadCoefficients warning is emitted.

    .. doctest::

        >>> import scipy.signal
        >>> from spectrum.transfer import tf2zpk
        >>> [b, a] = scipy.signal.butter(3.,.4)
        >>> z, p ,k = tf2zpk(b,a)

    .. seealso:: :func:`zpk2tf`
    .. note:: wrapper of scipy function tf2zpk
    """
    import scipy.signal
    z,p,k = scipy.signal.tf2zpk(b, a)
    return z,p,k