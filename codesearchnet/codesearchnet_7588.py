def speriodogram(x, NFFT=None, detrend=True, sampling=1.,
                   scale_by_freq=True, window='hamming', axis=0):
    """Simple periodogram, but matrices accepted.

    :param x: an array or matrix of data samples.
    :param NFFT: length of the data before FFT is computed (zero padding)
    :param bool detrend: detrend the data before co,puteing the FFT
    :param float sampling: sampling frequency of the input :attr:`data`.

    :param scale_by_freq:
    :param str window:

    :return: 2-sided PSD if complex data, 1-sided if real.

    if a matrix is provided (using numpy.matrix), then a periodogram
    is computed for each row. The returned matrix has the same shape as the input
    matrix.

    The mean of the input data is also removed from the data before computing
    the psd.

    .. plot::
        :width: 80%
        :include-source:

        from pylab import grid, semilogy
        from spectrum import data_cosine, speriodogram
        data = data_cosine(N=1024, A=0.1, sampling=1024, freq=200)
        semilogy(speriodogram(data, detrend=False, sampling=1024), marker='o')
        grid(True)


    .. plot::
        :width: 80%
        :include-source:

        import numpy
        from spectrum import speriodogram, data_cosine
        from pylab import figure, semilogy, figure ,imshow
        # create N data sets and make the frequency dependent on the time
        N = 100
        m = numpy.concatenate([data_cosine(N=1024, A=0.1, sampling=1024, freq=x) 
            for x in range(1, N)]);
        m.resize(N, 1024)
        res = speriodogram(m)
        figure(1)
        semilogy(res)
        figure(2)
        imshow(res.transpose(), aspect='auto')

    .. todo:: a proper spectrogram class/function that takes care of normalisation
    """
    x = np.array(x)
    # array with 1 dimension case
    if x.ndim == 1:
        axis = 0
        r = x.shape[0]
        w = Window(r, window)   #same size as input data
        w = w.data
    # matrix case
    elif x.ndim == 2:
        logging.debug('2D array. each row is a 1D array')
        [r, c] = x.shape
        w = np.array([Window(r, window).data for this in range(c)]).reshape(r,c) 

    if NFFT is None:
        NFFT = len(x)

    isreal = np.isrealobj(x)

    if detrend == True:
        m = np.mean(x, axis=axis)
    else:
        m = 0

    if isreal == True:
        if x.ndim == 2:
            res =  (abs (rfft (x*w - m, NFFT, axis=0))) ** 2. / r
        else:
            res =  (abs (rfft (x*w - m, NFFT, axis=-1))) ** 2. / r
    else:
        if x.ndim == 2:
            res =  (abs (fft (x*w - m, NFFT, axis=0))) ** 2. / r
        else:
            res =  (abs (fft (x*w - m, NFFT, axis=-1))) ** 2. / r

    if scale_by_freq is True:
        df = sampling / float(NFFT)
        res*= 2 * np.pi / df

    if x.ndim == 1:
        return res.transpose()
    else:
        return res