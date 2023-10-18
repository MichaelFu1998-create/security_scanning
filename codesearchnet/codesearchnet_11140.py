def count_fingerprint(word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
    """Return the count fingerprint.

    This is a wrapper for :py:meth:`Count.fingerprint`.

    Parameters
    ----------
    word : str
        The word to fingerprint
    n_bits : int
        Number of bits in the fingerprint returned
    most_common : list
        The most common tokens in the target language, ordered by frequency

    Returns
    -------
    int
        The count fingerprint

    Examples
    --------
    >>> bin(count_fingerprint('hat'))
    '0b1010000000001'
    >>> bin(count_fingerprint('niall'))
    '0b10001010000'
    >>> bin(count_fingerprint('colin'))
    '0b101010000'
    >>> bin(count_fingerprint('atcg'))
    '0b1010000000000'
    >>> bin(count_fingerprint('entreatment'))
    '0b1111010000100000'

    """
    return Count().fingerprint(word, n_bits, most_common)