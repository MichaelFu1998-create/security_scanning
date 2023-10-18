def occurrence_halved_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence halved fingerprint.

    This is a wrapper for :py:meth:`OccurrenceHalved.fingerprint`.

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
        The occurrence halved fingerprint

    Examples
    --------
    >>> bin(occurrence_halved_fingerprint('hat'))
    '0b1010000000010'
    >>> bin(occurrence_halved_fingerprint('niall'))
    '0b10010100000'
    >>> bin(occurrence_halved_fingerprint('colin'))
    '0b1001010000'
    >>> bin(occurrence_halved_fingerprint('atcg'))
    '0b10100000000000'
    >>> bin(occurrence_halved_fingerprint('entreatment'))
    '0b1111010000110000'

    """
    return OccurrenceHalved().fingerprint(word, n_bits, most_common)