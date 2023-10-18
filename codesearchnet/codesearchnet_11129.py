def occurrence_fingerprint(
    word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG
):
    """Return the occurrence fingerprint.

    This is a wrapper for :py:meth:`Occurrence.fingerprint`.

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
        The occurrence fingerprint

    Examples
    --------
    >>> bin(occurrence_fingerprint('hat'))
    '0b110000100000000'
    >>> bin(occurrence_fingerprint('niall'))
    '0b10110000100000'
    >>> bin(occurrence_fingerprint('colin'))
    '0b1110000110000'
    >>> bin(occurrence_fingerprint('atcg'))
    '0b110000000010000'
    >>> bin(occurrence_fingerprint('entreatment'))
    '0b1110010010000100'

    """
    return Occurrence().fingerprint(word, n_bits, most_common)