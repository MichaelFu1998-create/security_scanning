def examine_unexplained_noise(state, bins=1000, xlim=(-10,10)):
    """
    Compares a state's residuals in real and Fourier space with a Gaussian.

    Point out that Fourier space should always be Gaussian and white

    Parameters
    ----------
        state : `peri.states.State`
            The state to examine.
        bins : int or sequence of scalars or str, optional
            The number of bins in the histogram, as passed to numpy.histogram
            Default is 1000
        xlim : 2-element tuple, optional
            The range, in sigma, of the x-axis on the plot. Default (-10,10).

    Returns
    -------
        list
            The axes handles for the real and Fourier space subplots.
    """
    r = state.residuals
    q = np.fft.fftn(r)
    #Get the expected values of `sigma`:
    calc_sig = lambda x: np.sqrt(np.dot(x,x) / x.size)
    rh, xr = np.histogram(r.ravel() / calc_sig(r.ravel()), bins=bins,
            density=True)
    bigq = np.append(q.real.ravel(), q.imag.ravel())
    qh, xq = np.histogram(bigq / calc_sig(q.real.ravel()), bins=bins,
            density=True)
    xr = 0.5*(xr[1:] + xr[:-1])
    xq = 0.5*(xq[1:] + xq[:-1])

    gauss = lambda t : np.exp(-t*t*0.5) / np.sqrt(2*np.pi)

    plt.figure(figsize=[16,8])
    axes = []
    for a, (x, r, lbl) in enumerate([[xr, rh, 'Real'], [xq, qh, 'Fourier']]):
        ax = plt.subplot(1,2,a+1)
        ax.semilogy(x, r, label='Data')
        ax.plot(x, gauss(x), label='Gauss Fit', scalex=False, scaley=False)
        ax.set_xlabel('Residuals value $r/\sigma$')
        ax.set_ylabel('Probability $P(r/\sigma)$')
        ax.legend(loc='upper right')
        ax.set_title('{}-Space'.format(lbl))
        ax.set_xlim(xlim)
        axes.append(ax)
    return axes