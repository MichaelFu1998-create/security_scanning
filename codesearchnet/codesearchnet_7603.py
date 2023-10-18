def arma_estimate(X, P, Q, lag):
    """Autoregressive and moving average estimators.

    This function provides an estimate of the autoregressive
    parameters, the moving average parameters, and the driving
    white noise variance of  an ARMA(P,Q) for a complex or real data sequence.

    The parameters are estimated using three steps:

        * Estimate the AR parameters from the original data based on a least
          squares modified Yule-Walker technique,
        * Produce a residual time sequence by filtering the original data
          with a filter based on the AR parameters,
        * Estimate the MA parameters from the residual time sequence.

    :param array X: Array of data samples (length N)
    :param int P: Desired number of AR parameters
    :param int Q: Desired number of MA parameters
    :param int lag: Maximum lag to use for autocorrelation estimates

    :return:
        * A     - Array of complex P AR parameter estimates
        * B     - Array of complex Q MA parameter estimates
        * RHO   - White noise variance estimate

    .. note::
      *  lag must be >= Q (MA order)

    **dependencies**:
        * :meth:`spectrum.correlation.CORRELATION`
        * :meth:`spectrum.covar.arcovar`
        * :meth:`spectrum.arma.ma`

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import arma_estimate, arma2psd, marple_data
        import pylab

        a,b, rho = arma_estimate(marple_data, 15, 15, 30)
        psd = arma2psd(A=a, B=b, rho=rho, sides='centerdc', norm=True)
        pylab.plot(10 * pylab.log10(psd))
        pylab.ylim([-50,0])

    :reference: [Marple]_
    """
    R = CORRELATION(X, maxlags=lag, norm='unbiased')
    R0 = R[0]
    #C   Estimate the AR parameters (no error weighting is used).
    #C   Number of equation errors is M-Q .
    MPQ = lag - Q + P

    N = len(X)
    Y = np.zeros(N-P, dtype=complex)

    for K in range(0, MPQ):
        KPQ = K + Q - P+1
        if KPQ < 0:
            Y[K] = R[-KPQ].conjugate()
        if KPQ == 0:
            Y[K] = R0
        if KPQ > 0:
            Y[K] = R[KPQ]

    # The resize is very important for the normalissation.
    Y.resize(lag)
    if P <= 4:
        res = arcovar_marple(Y.copy(), P)    #! Eq. (10.12)
        ar_params = res[0]
    else:
        res = arcovar(Y.copy(), P)    #! Eq. (10.12)
        ar_params = res[0]

    # the .copy is used to prevent a reference somewhere. this is a bug
    # to be tracked down.
    Y.resize(N-P)

    #C   Filter the original time series
    for k in range(P, N):
        SUM = X[k]
        #SUM += sum([ar_params[j]*X[k-j-1] for j in range(0,P)])
        for j in range(0, P):
            SUM = SUM + ar_params[j] * X[k-j-1]   #! Eq. (10.17)
        Y[k-P] = SUM

    #  Estimate the MA parameters (a "long" AR of order at least 2*IQ
    #C   is suggested)
    #Y.resize(N-P)
    ma_params, rho = ma(Y, Q, 2*Q)     #! Eq. (10.3)

    return ar_params, ma_params, rho