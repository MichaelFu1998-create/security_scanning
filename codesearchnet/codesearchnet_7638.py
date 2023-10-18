def window_taylor(N, nbar=4, sll=-30):
    """Taylor tapering window

    Taylor windows allows you to make tradeoffs between the
    mainlobe width and sidelobe level (sll).

    Implemented as described by Carrara, Goodman, and Majewski 
    in 'Spotlight Synthetic Aperture Radar: Signal Processing Algorithms'
    Pages 512-513

    :param N: window length
    :param float nbar:
    :param float sll:

    The default values gives equal height
    sidelobes (nbar) and maximum sidelobe level (sll).

    .. warning:: not implemented

    .. seealso:: :func:`create_window`, :class:`Window`
    """
    B = 10**(-sll/20)
    A = log(B + sqrt(B**2 - 1))/pi
    s2 = nbar**2 / (A**2 + (nbar - 0.5)**2)
    ma = arange(1,nbar)
    def calc_Fm(m):
        numer = (-1)**(m+1) * prod(1-m**2/s2/(A**2 + (ma - 0.5)**2))
        denom = 2* prod([ 1-m**2/j**2 for j in ma if j != m])
        return numer/denom
    Fm = array([calc_Fm(m) for m in ma])
    def W(n):
        return 2 * np.sum(Fm * cos(2*pi*ma*(n-N/2 + 1/2)/N)) + 1
    w = array([W(n) for n in range(N)])
    # normalize (Note that this is not described in the original text)
    scale = W((N-1)/2)
    w /= scale
    return w