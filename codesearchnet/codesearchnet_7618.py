def zpk2ss(z, p, k):
    """Zero-pole-gain representation to state-space representation

    :param sequence z,p: Zeros and poles.
    :param float k: System gain.

    :return:
        * A, B, C, D : ndarray State-space matrices.

    .. note:: wrapper of scipy function zpk2ss
    """
    import scipy.signal
    return scipy.signal.zpk2ss(z,p,k)