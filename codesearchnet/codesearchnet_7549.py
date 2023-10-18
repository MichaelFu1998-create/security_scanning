def twosided_2_onesided(data):
    """Convert a one-sided PSD to a twosided PSD

    In order to keep the power in the onesided PSD the same
    as in the twosided version, the onesided values are twice
    as much as in the input data (except for the zero-lag value).

    ::

        >>> twosided_2_onesided([10, 2,3,3,2,8])
        array([ 10.,   4.,   6.,   8.])

    """
    assert len(data) % 2 == 0
    N = len(data)
    psd = np.array(data[0:N//2+1]) * 2.
    psd[0] /= 2.
    psd[-1] = data[-1]
    return psd