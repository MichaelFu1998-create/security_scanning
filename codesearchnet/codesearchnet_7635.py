def window_tukey(N, r=0.5):
    """Tukey tapering window (or cosine-tapered window)

    :param N: window length
    :param r: defines the ratio between the constant section and the cosine
      section. It has to be between 0 and 1.

    The function returns a Hanning window for `r=0` and a full box for `r=1`.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import window_visu
        window_visu(64, 'tukey')
        window_visu(64, 'tukey', r=1)

    .. math:: 0.5 (1+cos(2pi/r (x-r/2))) for 0<=x<r/2

    .. math:: 0.5 (1+cos(2pi/r (x-1+r/2))) for x>=1-r/2


    .. seealso:: :func:`create_window`, :class:`Window`
    """
    assert r>=0 and r<=1 , "r must be in [0,1]"
    if N==1:
        return ones(1)

    if r == 0:
        return ones(N)
    elif r == 1:
        return window_hann(N)
    else:
        from numpy import flipud, concatenate, where

        ## cosine-tapered window
        x = linspace(0, 1, N)
        x1 = where(x<r/2.)
        w = 0.5*(1+cos(2*pi/r*(x[x1[0]]-r/2)))
        w = concatenate((w, ones(N-len(w)*2), flipud(w)))


        return w