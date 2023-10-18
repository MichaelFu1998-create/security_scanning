def ss2zpk(a,b,c,d, input=0):
    """State-space representation to zero-pole-gain representation.

    :param A: ndarray State-space representation of linear system.
    :param B: ndarray State-space representation of linear system.
    :param C: ndarray State-space representation of linear system.
    :param D: ndarray State-space representation of linear system.
    :param int input: optional For multiple-input systems, the input to use.

    :return:
        * z, p : sequence  Zeros and poles.
        * k : float System gain.

    .. note:: wrapper of scipy function ss2zpk
    """
    import scipy.signal
    z, p, k = scipy.signal.ss2zpk(a, b, c, d, input=input)
    return z, p, k