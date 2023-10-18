def modcovar(x, order):
    """Simple and fast implementation of the covariance AR estimate

    This code is 10 times faster than :func:`modcovar_marple` and more importantly
    only 10 lines of code, compared to a 200 loc for :func:`modcovar_marple`

    :param X:        Array of complex data samples
    :param int order:   Order of linear prediction model

    :return:
        * P    - Real linear prediction variance at order IP
        * A    - Array of complex linear prediction coefficients


    .. plot::
        :include-source:
        :width: 80%

        from spectrum import modcovar, marple_data, arma2psd, cshift
        from pylab import log10, linspace, axis, plot 

        a, p = modcovar(marple_data, 15)
        PSD = arma2psd(a)
        PSD = cshift(PSD, len(PSD)/2) # switch positive and negative freq
        plot(linspace(-0.5, 0.5, 4096), 10*log10(PSD/max(PSD)))
        axis([-0.5,0.5,-60,0])

    .. seealso:: :class:`~spectrum.modcovar.pmodcovar`

    :validation: the AR parameters are the same as those returned by
        a completely different function :func:`modcovar_marple`.


    :References: Mathworks
    """
    from spectrum import corrmtx
    import scipy.linalg
    X = corrmtx(x, order, 'modified')
    Xc = np.matrix(X[:,1:])
    X1 = np.array(X[:,0])

    # Coefficients estimated via the covariance method
    # Here we use lstsq rathre than solve function because Xc is not square matrix
    a, residues, rank, singular_values = scipy.linalg.lstsq(-Xc, X1)

    # Estimate the input white noise variance


    Cz = np.dot(X1.conj().transpose(), Xc)
    e = np.dot(X1.conj().transpose(), X1) + np.dot(Cz, a)
    assert e.imag < 1e-4, 'wierd behaviour'
    e = float(e.real) # ignore imag part that should be small

    return a, e