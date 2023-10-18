def centerdc_2_twosided(data):
    """Convert a center-dc PSD to a twosided PSD"""
    N = len(data)
    newpsd = np.concatenate((data[N//2:], (cshift(data[0:N//2], -1))))
    return newpsd