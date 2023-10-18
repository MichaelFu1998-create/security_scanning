def ma(X, Q, M):
    """Moving average estimator.

    This program provides an estimate of the moving average parameters
    and driving noise variance for a data sequence based on a
    long AR model and a least squares fit.

    :param array X: The input data array
    :param int Q: Desired MA model order (must be >0 and <M)
    :param int M: Order of "long" AR model (suggest at least 2*Q )

    :return:
        * MA    - Array of Q complex MA parameter estimates
        * RHO   - Real scalar of white noise variance estimate

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import arma2psd, ma, marple_data
        import pylab

        # Estimate 15 Ma parameters
        b, rho = ma(marple_data, 15, 30)
        # Create the PSD from those MA parameters
        psd = arma2psd(B=b, rho=rho, sides='centerdc')
        # and finally plot the PSD
        pylab.plot(pylab.linspace(-0.5, 0.5, 4096), 10 * pylab.log10(psd/max(psd)))
        pylab.axis([-0.5, 0.5, -30, 0])

    :reference: [Marple]_
    """
    if Q <= 0 or Q >= M:
        raise ValueError('Q(MA) must be in ]0,lag[')

    #C   Fit a high-order AR to the data
    a, rho, _c = yulewalker.aryule(X, M, 'biased')   #! Eq. (10.5)

    #add an element unity to the AR parameter array
    a = np.insert(a, 0, 1)

    #C   Find MA parameters from autocorrelations by Yule-Walker method
    ma_params, _p, _c = yulewalker.aryule(a, Q, 'biased')    #! Eq. (10.7)

    return ma_params, rho