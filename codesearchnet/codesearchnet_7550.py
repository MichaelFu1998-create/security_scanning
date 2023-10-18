def onesided_2_twosided(data):
    """Convert a two-sided PSD to a one-sided PSD

    In order to keep the power in the twosided PSD the same
    as in the onesided version, the twosided values are 2 times
    lower than the input data (except for the zero-lag and N-lag
    values).

    ::

        >>> twosided_2_onesided([10, 4, 6, 8])
        array([ 10.,   2.,   3.,   3., 2., 8.])

    """
    psd = np.concatenate((data[0:-1], cshift(data[-1:0:-1], -1)))/2.
    psd[0] *= 2.
    psd[-1] *= 2.
    return psd