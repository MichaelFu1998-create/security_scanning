def lar2rc(g):
    """Convert log area ratios to reflection coefficients.

    :param g:  log area ratios
    :returns: the reflection coefficients

    .. seealso: :func:`rc2lar`, :func:`poly2rc`, :func:`ac2rc`, :func:`is2rc`.

    :References:
       [1] J. Makhoul, "Linear Prediction: A Tutorial Review," Proc. IEEE,  Vol.63, No.4, pp.561-580, Apr 1975.

    """
    assert numpy.isrealobj(g), 'Log area ratios not defined for complex reflection coefficients.'
    # Use the relation, tanh(x) = (1-exp(2x))/(1+exp(2x))
    return -numpy.tanh(-numpy.array(g)/2)