def phonetic_fingerprint(
    phrase, phonetic_algorithm=double_metaphone, joiner=' ', *args, **kwargs
):
    """Return the phonetic fingerprint of a phrase.

    This is a wrapper for :py:meth:`Phonetic.fingerprint`.

    Parameters
    ----------
    phrase : str
        The string from which to calculate the phonetic fingerprint
    phonetic_algorithm : function
        A phonetic algorithm that takes a string and returns a string
        (presumably a phonetic representation of the original string). By
        default, this function uses :py:func:`.double_metaphone`.
    joiner : str
        The string that will be placed between each word
    *args
        Variable length argument list
    **kwargs
        Arbitrary keyword arguments

    Returns
    -------
    str
        The phonetic fingerprint of the phrase

    Examples
    --------
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.')
    '0 afr fks jmpt kk ls prn tk'
    >>> from abydos.phonetic import soundex
    >>> phonetic_fingerprint('The quick brown fox jumped over the lazy dog.',
    ... phonetic_algorithm=soundex)
    'b650 d200 f200 j513 l200 o160 q200 t000'

    """
    return Phonetic().fingerprint(
        phrase, phonetic_algorithm, joiner, *args, **kwargs
    )