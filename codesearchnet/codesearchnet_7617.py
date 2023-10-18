def zpk2tf(z, p, k):
    r"""Return polynomial transfer function representation from zeros and poles

    :param ndarray z: Zeros of the transfer function.
    :param ndarray p: Poles of the transfer function.
    :param float k: System gain.

    :return:
        b : ndarray Numerator polynomial.
        a : ndarray Numerator and denominator polynomials.

    :func:`zpk2tf` forms transfer function polynomials from the zeros, poles, and gains
    of a system in factored form.

    zpk2tf(z,p,k) finds a rational transfer function

    .. math:: \frac{B(s)}{A(s)} = \frac{b_1 s^{n-1}+\dots b_{n-1}s+b_n}{a_1 s^{m-1}+\dots a_{m-1}s+a_m}

    given a system in factored transfer function form

    .. math:: H(s) = \frac{Z(s)}{P(s)} = k \frac{(s-z_1)(s-z_2)\dots(s-z_m)}{(s-p_1)(s-p_2)\dots(s-p_n)}


    with p being the pole locations, and z the zero locations, with as many.
    The gains for each numerator transfer function are in vector k.
    The zeros and poles must be real or come in complex conjugate pairs.
    The polynomial denominator coefficients are returned in row vector a and
    the polynomial numerator coefficients are returned in matrix b, which has
    as many rows as there are columns of z.

    Inf values can be used as place holders in z if some columns have fewer zeros than others.

    .. note:: wrapper of scipy function zpk2tf
    """
    import scipy.signal
    b, a = scipy.signal.zpk2tf(z, p, k)
    return b, a