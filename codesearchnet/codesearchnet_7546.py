def lsf2poly(lsf):
    """Convert line spectral frequencies to prediction filter coefficients

    returns a vector a containing the prediction filter coefficients from a vector lsf of line spectral frequencies.

    .. doctest::

        >>> from spectrum import lsf2poly
        >>> lsf = [0.7842 ,   1.5605  ,  1.8776 ,   1.8984,    2.3593]
        >>> a = lsf2poly(lsf)

    # array([  1.00000000e+00,   6.14837835e-01,   9.89884967e-01,
    # 9.31594056e-05,   3.13713832e-03,  -8.12002261e-03 ])

    .. seealso:: poly2lsf, rc2poly, ac2poly, rc2is
    """
    #   Reference: A.M. Kondoz, "Digital Speech: Coding for Low Bit Rate Communications
    #   Systems" John Wiley & Sons 1994 ,Chapter 4

    # Line spectral frequencies must be real.

    lsf = numpy.array(lsf)

    if max(lsf) > numpy.pi or min(lsf) < 0:
        raise ValueError('Line spectral frequencies must be between 0 and pi.')

    p = len(lsf) # model order

    # Form zeros using the LSFs and unit amplitudes
    z  = numpy.exp(1.j * lsf)

    # Separate the zeros to those belonging to P and Q
    rQ = z[0::2]
    rP = z[1::2]

    # Include the conjugates as well
    rQ = numpy.concatenate((rQ, rQ.conjugate()))
    rP = numpy.concatenate((rP, rP.conjugate()))

    # Form the polynomials P and Q, note that these should be real
    Q  = numpy.poly(rQ);
    P  = numpy.poly(rP);

    # Form the sum and difference filters by including known roots at z = 1 and
    # z = -1

    if p%2:
        # Odd order: z = +1 and z = -1 are roots of the difference filter, P1(z)
        P1 = numpy.convolve(P, [1, 0, -1])
        Q1 = Q
    else:
        # Even order: z = -1 is a root of the sum filter, Q1(z) and z = 1 is a
        # root of the difference filter, P1(z)
        P1 = numpy.convolve(P, [1, -1])
        Q1 = numpy.convolve(Q, [1,  1])

    # Prediction polynomial is formed by averaging P1 and Q1

    a = .5 * (P1+Q1)
    return a[0:-1:1]