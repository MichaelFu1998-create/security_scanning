def window_parzen(N):
    r"""Parsen tapering window (also known as de la Valle-Poussin)

    :param N: window length

    Parzen windows are piecewise cubic approximations
    of Gaussian windows. Parzen window sidelobes fall off as :math:`1/\omega^4`.

    if :math:`0\leq|x|\leq (N-1)/4`:

    .. math:: w(n) = 1-6 \left( \frac{|n|}{N/2} \right)^2 +6 \left( \frac{|n|}{N/2}\right)^3

    if :math:`(N-1)/4\leq|x|\leq (N-1)/2`

    .. math:: w(n) = 2 \left(1- \frac{|n|}{N/2}\right)^3


    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'parzen')


    .. seealso:: :func:`create_window`, :class:`Window`
    """
    from numpy import  where, concatenate

    n = linspace(-(N-1)/2., (N-1)/2., N)
    n1 = n[where(abs(n)<=(N-1)/4.)[0]]
    n2 = n[where(n>(N-1)/4.)[0]]
    n3 = n[where(n<-(N-1)/4.)[0]]


    w1 = 1. -6.*(abs(n1)/(N/2.))**2 + 6*(abs(n1)/(N/2.))**3
    w2 = 2.*(1-abs(n2)/(N/2.))**3
    w3 = 2.*(1-abs(n3)/(N/2.))**3

    w = concatenate((w3, w1, w2))
    return w