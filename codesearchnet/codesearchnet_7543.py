def rc2is(k):
    """Convert reflection coefficients to inverse sine parameters.

    :param k: reflection coefficients
    :return: inverse sine parameters

    .. seealso:: :func:`is2rc`, :func:`rc2poly`, :func:`rc2acC`, :func:`rc2lar`.

    Reference: J.R. Deller, J.G. Proakis, J.H.L. Hansen, "Discrete-Time
       Processing of Speech Signals", Prentice Hall, Section 7.4.5.

    """
    assert numpy.isrealobj(k), 'Inverse sine parameters not defined for complex reflection coefficients.'
    if max(numpy.abs(k)) >= 1:
        raise ValueError('All reflection coefficients should have magnitude less than unity.')

    return (2/numpy.pi)*numpy.arcsin(k)