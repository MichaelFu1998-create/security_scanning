def _coeff4(N, a0, a1, a2, a3):
    """a common internal function to some window functions with 4 coeffs


    For the blackmna harris for instance, the results are identical to octave if N is odd
    but not for even values...if n =0 whatever N is, the w(0) must be equal to a0-a1+a2-a3, which
    is the case here, but not in octave..."""
    if N == 1:
        return ones(1)

    n = arange(0, N)
    N1 = N - 1.

    w = a0 -a1*cos(2.*pi*n / N1) + a2*cos(4.*pi*n / N1) - a3*cos(6.*pi*n / N1)

    return w