def position_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG, bits_per_letter=3
):
    """Return the position fingerprint.

    This is a wrapper for :py:meth:`Position.fingerprint`.

    Parameters
    ----------
    word : str
        The word to fingerprint
    n_bits : int
        Number of bits in the fingerprint returned
    most_common : list
        The most common tokens in the target language, ordered by frequency
    bits_per_letter : int
        The bits to assign for letter position

    Returns
    -------
    int
        The position fingerprint

    Examples
    --------
    >>> bin(position_fingerprint('hat'))
    '0b1110100011111111'
    >>> bin(position_fingerprint('niall'))
    '0b1111110101110010'
    >>> bin(position_fingerprint('colin'))
    '0b1111111110010111'
    >>> bin(position_fingerprint('atcg'))
    '0b1110010001111111'
    >>> bin(position_fingerprint('entreatment'))
    '0b101011111111'

    """
    return Position().fingerprint(word, n_bits, most_common, bits_per_letter)