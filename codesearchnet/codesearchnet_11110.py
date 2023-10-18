def ac_decode(longval, nbits, probs):
    """Decode the number to a string using the given statistics.

    This is a wrapper for :py:meth:`Arithmetic.decode`.

    Parameters
    ----------
    longval : int
        The first part of an encoded tuple from ac_encode
    nbits : int
        The second part of an encoded tuple from ac_encode
    probs : dict
        A probability statistics dictionary generated by
        :py:meth:`Arithmetic.train`

    Returns
    -------
    str
        The arithmetically decoded text

    Example
    -------
    >>> pr = ac_train('the quick brown fox jumped over the lazy dog')
    >>> ac_decode(16720586181, 34, pr)
    'align'

    """
    coder = Arithmetic()
    coder.set_probs(probs)
    return coder.decode(longval, nbits)