def dpss(N, NW=None, k=None):
    r"""Discrete prolate spheroidal (Slepian) sequences

    Calculation of the Discrete Prolate Spheroidal Sequences also known as the
    slepian sequences, and the corresponding eigenvalues.

    :param int N: desired window length
    :param float NW: The time half bandwidth parameter (typical values are
        2.5,3,3.5,4).
    :param int k: returns the first k Slepian sequences. If *k* is not
        provided, *k* is set to *NW*2*.
    :return:
        * tapers, a matrix of tapering windows. Matrix is a N by *k* (k
          is the number of windows)
        * eigen, a vector of eigenvalues of length *k*

    The discrete prolate spheroidal or Slepian sequences derive from the following
    time-frequency concentration problem. For all finite-energy sequences index
    limited to some set , which sequence maximizes the following ratio:

    .. math::

        \lambda = \frac{\int_{-W}^{W}\left| X(f) \right|^2 df}
            {\int_{-F_s/2}^{F_s/2}\left| X(f) \right|^2 df}

    where :math:`F_s` is the sampling frequency and :math:`|W| < F_s/2`.
    This ratio determines which index-limited sequence has the largest proportion of its
    energy in the band :math:`[-W,W]` with :math:`0  < \lambda < 1`.
    The sequence maximizing the ratio is the first
    discrete prolate spheroidal or Slepian sequence. The second Slepian sequence
    maximizes the ratio and is orthogonal to the first Slepian sequence. The third
    Slepian sequence maximizes the ratio of integrals and is orthogonal to both
    the first and second Slepian sequences and so on.

    .. note:: Note about the implementation. Since the slepian generation is
        computationally expensive, we use a C implementation based on the C
        code written by Lees as published in:

            Lees, J. M. and J. Park (1995): Multiple-taper spectral analysis: A stand-alone
            C-subroutine: Computers & Geology: 21, 199-236.

        However, the original C code has been trimmed. Indeed, we only require the
        multitap function (that depends on jtridib, jtinvit functions only).

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import *
        from pylab import *
        N = 512
        [w, eigens] = dpss(N, 2.5, 4)
        plot(w)
        title('Slepian Sequences N=%s, NW=2.5' % N)
        axis([0, N, -0.15, 0.15])
        legend(['1st window','2nd window','3rd window','4th window'])

    Windows are normalised:

    .. math::  \sum_k h_k h_k = 1

    :references: [Percival]_

        Slepian, D. Prolate spheroidal wave functions, Fourier analysis, and
        uncertainty V: The discrete case. Bell System Technical Journal,
        Volume 57 (1978), 1371430

    .. note:: the C code to create the slepian windows is extracted from original C code
        from Lees and Park (1995) and uses the conventions of Percival and Walden (1993).
        Functions that are not used here were removed.

    """
    assert NW < N/2 , "NW ({}) must be stricly less than N/2 ({}/2)".format(NW, N)
    if k is None:
        k = min(round(2*NW),N)
        k = int(max(k,1))
    from numpy import dot, zeros, arange, sqrt
    mtspeclib.multitap.restype = None

    lam = zeros(k, dtype=float)
    tapers = zeros(k*N, dtype=float)
    tapsum = zeros(k, dtype=float)

    res = mtspeclib.multitap(
        c_int(N),
        c_int(k),
        lam.ctypes.data_as(c_void_p),
        c_float(NW),
        tapers.ctypes.data_as(c_void_p),
        tapsum.ctypes.data_as(c_void_p),
        )

    # normalisation by sqtr(N). It is required to have normalised windows
    tapers = tapers.reshape(k,N).transpose() / sqrt(N)

    for i in range(k):
        # By convention (Percival and Walden, 1993 pg 379)
        # * symmetric tapers (k=0,2,4,...) should have a positive average.
        # * antisymmetric tapers should begin with a positive lobe
        if i%2 == 0:
            if tapsum[i]<0:
                tapsum[i] *= -1
                tapers[:,i] *= -1
        else:
            if tapers[0,i] < 0:
                tapsum[i] *= -1
                tapers[:,i] *= -1

    # Now find the eigenvalues of the original
    # Use the autocovariance sequence technique from Percival and Walden, 1993
    # pg 390 to get the eigenvalues more precisely (same as matlab output)

    # The values returned in lam are not exacly the same as in the following methods.
    acvs = _autocov(tapers.transpose(), debias=False) * N
    nidx = arange(N)
    W = float(NW)/N
    r = 4*W*np.sinc(2*W*nidx)
    r[0] = 2*W
    eigvals = dot(acvs, r)

    #return (tapers, lam)
    return [tapers, eigvals]