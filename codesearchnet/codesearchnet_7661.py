def arcovar(x, order):
    r"""Simple and fast implementation of the covariance AR estimate

    This code is 10 times faster than :func:`arcovar_marple` and more importantly
    only 10 lines of code, compared to a 200 loc for :func:`arcovar_marple`


    :param array X:  Array of complex data samples
    :param int oder: Order of linear prediction model

    :return:
        * a - Array of complex forward linear prediction coefficients
        * e - error

    The covariance method fits a Pth order autoregressive (AR) model to the
    input signal, which is assumed to be the output of
    an AR system driven by white noise. This method minimizes the forward
    prediction error in the least-squares sense. The output vector
    contains the normalized estimate of the AR system parameters

    The white noise input variance estimate is also returned.

    If is the power spectral density of y(n), then:

    .. math:: \frac{e}{\left| A(e^{jw}) \right|^2} = \frac{e}{\left| 1+\sum_{k-1}^P a(k)e^{-jwk}\right|^2}

    Because the method characterizes the input data using an all-pole model,
    the correct choice of the model order p is important.

    .. plot::
        :width: 80%
        :include-source:

        from spectrum import arcovar, marple_data, arma2psd
        from pylab import plot, log10, linspace, axis

        ar_values, error = arcovar(marple_data, 15)
        psd = arma2psd(ar_values, sides='centerdc')
        plot(linspace(-0.5, 0.5, len(psd)), 10*log10(psd/max(psd)))
        axis([-0.5, 0.5, -60, 0])

    .. seealso:: :class:`pcovar`

    :validation: the AR parameters are the same as those returned by
        a completely different function :func:`arcovar_marple`.

    :References: [Mathworks]_
    """

    from spectrum import corrmtx
    import scipy.linalg

    X = corrmtx(x, order, 'covariance')
    Xc = np.matrix(X[:, 1:])
    X1 = np.array(X[:, 0])

    # Coefficients estimated via the covariance method
    # Here we use lstsq rathre than solve function because Xc is not square
    # matrix

    a, _residues, _rank, _singular_values = scipy.linalg.lstsq(-Xc, X1)

    # Estimate the input white noise variance
    Cz = np.dot(X1.conj().transpose(), Xc)
    e = np.dot(X1.conj().transpose(), X1) + np.dot(Cz, a)
    assert e.imag < 1e-4, 'wierd behaviour'
    e = float(e.real) # ignore imag part that should be small

    return a, e