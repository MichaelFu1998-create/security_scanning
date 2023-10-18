def rc2poly(kr, r0=None):
    """convert reflection coefficients to prediction filter polynomial

    :param k: reflection coefficients




    """
    # Initialize the recursion
    from .levinson import levup
    p = len(kr)              #% p is the order of the prediction polynomial.
    a = numpy.array([1, kr[0]])           #% a is a true polynomial.
    e = numpy.zeros(len(kr))

    if r0 is None:
        e0 = 0
    else:
        e0 = r0

    e[0] = e0 * (1. - numpy.conj(numpy.conjugate(kr[0])*kr[0]))

    # Continue the recursion for k=2,3,...,p, where p is the order of the
    # prediction polynomial.

    for k in range(1, p):
        [a, e[k]] = levup(a, kr[k], e[k-1])

    efinal = e[-1]
    return a, efinal