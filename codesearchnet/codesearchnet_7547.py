def poly2lsf(a):
    """Prediction polynomial to line spectral frequencies.

    converts the prediction polynomial specified by A,
    into the corresponding line spectral frequencies, LSF.
    normalizes the prediction polynomial by A(1).

    .. doctest::

        >>> from spectrum import poly2lsf
        >>> a = [1.0000,  0.6149, 0.9899, 0.0000 ,0.0031, -0.0082]
        >>> lsf = poly2lsf(a)
        >>> lsf =  array([0.7842, 1.5605, 1.8776, 1.8984, 2.3593])

    .. seealso:: lsf2poly, poly2rc, poly2qc, rc2is
    """

    #Line spectral frequencies are not defined for complex polynomials.

    # Normalize the polynomial

    a = numpy.array(a)
    if a[0] != 1:
        a/=a[0]

    if max(numpy.abs(numpy.roots(a))) >= 1.0:
        error('The polynomial must have all roots inside of the unit circle.');


    # Form the sum and differnce filters

    p  = len(a)-1   # The leading one in the polynomial is not used
    a1 = numpy.concatenate((a, numpy.array([0])))
    a2 = a1[-1::-1]
    P1 = a1 - a2        # Difference filter
    Q1 = a1 + a2        # Sum Filter

    # If order is even, remove the known root at z = 1 for P1 and z = -1 for Q1
    # If odd, remove both the roots from P1

    if p%2: # Odd order
        P, r = deconvolve(P1,[1, 0 ,-1])
        Q = Q1
    else:          # Even order
        P, r = deconvolve(P1, [1, -1])
        Q, r = deconvolve(Q1, [1,  1])

    rP  = numpy.roots(P)
    rQ  = numpy.roots(Q)

    aP  = numpy.angle(rP[1::2])
    aQ  = numpy.angle(rQ[1::2])

    lsf = sorted(numpy.concatenate((-aP,-aQ)))

    return lsf