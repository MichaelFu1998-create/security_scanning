def rc2lar(k):
    """Convert reflection coefficients to log area ratios.

    :param k: reflection coefficients
    :return: inverse sine parameters

    The log area ratio is defined by G = log((1+k)/(1-k)) , where the K
    parameter is the reflection coefficient.

    .. seealso:: :func:`lar2rc`, :func:`rc2poly`, :func:`rc2ac`, :func:`rc2ic`.

    :References:
       [1] J. Makhoul, "Linear Prediction: A Tutorial Review," Proc. IEEE, Vol.63, No.4, pp.561-580, Apr 1975.

    """
    assert numpy.isrealobj(k), 'Log area ratios not defined for complex reflection coefficients.'
    if max(numpy.abs(k)) >= 1:
        raise ValueError('All reflection coefficients should have magnitude less than unity.')

    # Use the relation, atanh(x) = (1/2)*log((1+k)/(1-k))
    return -2 * numpy.arctanh(-numpy.array(k))