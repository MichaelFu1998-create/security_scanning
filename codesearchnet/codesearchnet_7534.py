def CORRELATION(x, y=None, maxlags=None, norm='unbiased'):
    r"""Correlation function

    This function should give the same results as :func:`xcorr` but it
    returns the positive lags only. Moreover the algorithm does not use
    FFT as compared to other algorithms.

    :param array x: first data array of length N
    :param array y: second data array of length N. If not specified, computes the
        autocorrelation.
    :param int maxlags: compute cross correlation between [0:maxlags]
        when maxlags is not specified, the range of lags is [0:maxlags].
    :param str norm: normalisation in ['biased', 'unbiased', None, 'coeff']

        * *biased*   correlation=raw/N,
        * *unbiased* correlation=raw/(N-`|lag|`)
        * *coeff*    correlation=raw/(rms(x).rms(y))/N
        * None       correlation=raw

    :return:
        * a numpy.array correlation sequence,  r[1,N]
        * a float for the zero-lag correlation,  r[0]

    The *unbiased* correlation has the form:

    .. math::

        \hat{r}_{xx} = \frac{1}{N-m}T \sum_{n=0}^{N-m-1} x[n+m]x^*[n] T

    The *biased* correlation differs by the front factor only:

    .. math::

        \check{r}_{xx} = \frac{1}{N}T \sum_{n=0}^{N-m-1} x[n+m]x^*[n] T

    with :math:`0\leq m\leq N-1`.

    .. doctest::

        >>> from spectrum import CORRELATION
        >>> x = [1,2,3,4,5]
        >>> res = CORRELATION(x,x, maxlags=0, norm='biased')
        >>> res[0]
        11.0

    .. note:: this function should be replaced by :func:`xcorr`.

    .. seealso:: :func:`xcorr`
    """
    assert norm in ['unbiased','biased', 'coeff', None]
    #transform lag into list if it is an integer
    x = np.array(x)
    if y is None:
        y = x
    else:
        y = np.array(y)

    # N is the max of x and y
    N = max(len(x), len(y))
    if len(x) < N:
        x = y.copy()
        x.resize(N)
    if len(y) < N:
        y = y.copy()
        y.resize(N)

    #default lag is N-1
    if maxlags is None:
        maxlags = N - 1
    assert maxlags < N, 'lag must be less than len(x)'

    realdata = np.isrealobj(x) and np.isrealobj(y)
    #create an autocorrelation array with same length as lag
    if realdata == True:
        r = np.zeros(maxlags, dtype=float)
    else:
        r = np.zeros(maxlags, dtype=complex)

    if norm == 'coeff':
        rmsx = pylab_rms_flat(x)
        rmsy = pylab_rms_flat(y)

    for k in range(0, maxlags+1):
        nk = N - k - 1

        if realdata == True:
            sum = 0
            for j in range(0, nk+1):
                sum = sum + x[j+k] * y[j]
        else:
            sum = 0. + 0j
            for j in range(0, nk+1):
                sum = sum + x[j+k] * y[j].conjugate()
        if k == 0:
            if norm in ['biased', 'unbiased']:
                r0 = sum/float(N)
            elif norm is None:
                r0 = sum
            else:
                r0 =  1.
        else:
            if norm == 'unbiased':
                r[k-1] = sum / float(N-k)
            elif norm == 'biased':
                r[k-1] = sum / float(N)
            elif norm is None:
                r[k-1] = sum
            elif norm == 'coeff':
                r[k-1] =  sum/(rmsx*rmsy)/float(N)

    r = np.insert(r, 0, r0)
    return r