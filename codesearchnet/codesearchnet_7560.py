def pmtm(x, NW=None, k=None, NFFT=None, e=None, v=None, method='adapt', show=False):
    """Multitapering spectral estimation

    :param array x: the data
    :param float NW: The time half bandwidth parameter (typical values are
        2.5,3,3.5,4). Must be provided otherwise the tapering windows and
        eigen values (outputs of dpss) must be provided
    :param int k: uses the first k Slepian sequences. If *k* is not provided,
        *k* is set to *NW*2*.
    :param NW:
    :param e: the window concentrations (eigenvalues)
    :param v: the matrix containing the tapering windows
    :param str method: set how the eigenvalues are used. Must be
        in ['unity', 'adapt', 'eigen']
    :param bool show: plot results
    :return: Sk (complex), weights, eigenvalues

    Usually in spectral estimation the mean to reduce bias is to use tapering
    window. In order to reduce variance we need to average different spectrum.
    The problem is that we have only one set of data. Thus we need to
    decompose a set into several segments. Such method are well-known: simple
    daniell's periodogram, Welch's method and so on. The drawback of such
    methods is a loss of resolution since the segments used to compute the
    spectrum are smaller than the data set.
    The interest of multitapering method is to keep a good resolution while
    reducing bias and variance.

    How does it work? First we compute different simple periodogram with the
    whole data set (to keep good resolution) but each periodgram is computed
    with a differenttapering windows. Then, we average all these spectrum.
    To avoid redundancy and bias due to the tapers mtm use special tapers.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import data_cosine, dpss, pmtm

        data = data_cosine(N=2048, A=0.1, sampling=1024, freq=200)
        # If you already have the DPSS windows
        [tapers, eigen] = dpss(2048, 2.5, 4)
        res = pmtm(data, e=eigen, v=tapers, show=False)
        # You do not need to compute the DPSS before end
        res = pmtm(data, NW=2.5, show=False)
        res = pmtm(data, NW=2.5, k=4, show=True)


    .. versionchanged:: 0.6.2

        APN modified method to return each Sk as complex values, the eigenvalues
        and the weights

    """
    assert method in ['adapt','eigen','unity']

    N = len(x)

    # if dpss not provided, compute them
    if e is None and v is None:
        if NW is not None:
            [tapers, eigenvalues] = dpss(N, NW, k=k)
        else:
            raise ValueError("NW must be provided (e.g. 2.5, 3, 3.5, 4")
    elif e is not None and v is not None:
        eigenvalues = e[:]
        tapers = v[:]
    else:
        raise ValueError("if e provided, v must be provided as well and viceversa.")
    nwin = len(eigenvalues) # length of the eigen values vector to be used later

    # set the NFFT
    if NFFT==None:
        NFFT = max(256, 2**nextpow2(N))

    Sk_complex = np.fft.fft(np.multiply(tapers.transpose(), x), NFFT)
    Sk = abs(Sk_complex)**2

    # si nfft smaller thqn N, cut otherwise add wero.
    # compute
    if method in ['eigen', 'unity']:
        if method == 'unity':
            weights = np.ones((nwin, 1))
        elif method == 'eigen':
            # The S_k spectrum can be weighted by the eigenvalues, as in Park et al.
            weights = np.array([_x/float(i+1) for i,_x in enumerate(eigenvalues)])
            weights = weights.reshape(nwin,1)

    elif method == 'adapt':
        # This version uses the equations from [2] (P&W pp 368-370).

        # Wrap the data modulo nfft if N > nfft
        sig2 = np.dot(x, x) / float(N)
        Sk = abs(np.fft.fft(np.multiply(tapers.transpose(), x), NFFT))**2
        Sk = Sk.transpose()
        S = (Sk[:,0] + Sk[:,1]) / 2    # Initial spectrum estimate
        S = S.reshape(NFFT, 1)
        Stemp = np.zeros((NFFT,1))
        S1 = np.zeros((NFFT,1))
        # Set tolerance for acceptance of spectral estimate:
        tol = 0.0005 * sig2 / float(NFFT)
        i = 0
        a = sig2 * (1 - eigenvalues)

        # converges very quickly but for safety; set i<100
        while sum(np.abs(S-S1))/NFFT > tol and i<100:
            i = i + 1
            # calculate weights
            b1 = np.multiply(S, np.ones((1,nwin)))
            b2 = np.multiply(S,eigenvalues.transpose()) + np.ones((NFFT,1))*a.transpose()
            b = b1/b2

            # calculate new spectral estimate
            wk=(b**2)*(np.ones((NFFT,1))*eigenvalues.transpose())
            S1 = sum(wk.transpose()*Sk.transpose())/ sum(wk.transpose())
            S1 = S1.reshape(NFFT, 1)
            Stemp = S1
            S1 = S
            S = Stemp   # swap S and S1
        weights=wk

    if show is True:
        from pylab import semilogy
        if method == "adapt":
            Sk = np.mean(Sk * weights, axis=1)
        else:
            Sk = np.mean(Sk * weights, axis=0)
        semilogy(Sk)

    return Sk_complex, weights, eigenvalues