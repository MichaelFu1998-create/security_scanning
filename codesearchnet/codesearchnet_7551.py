def twosided_2_centerdc(data):
    """Convert a two-sided PSD to a center-dc PSD"""
    N = len(data)
    # could us int() or // in python 3
    newpsd = np.concatenate((cshift(data[N//2:], 1), data[0:N//2]))
    newpsd[0] = data[-1]
    return newpsd