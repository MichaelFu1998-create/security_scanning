def spanish_metaphone(word, max_length=6, modified=False):
    """Return the Spanish Metaphone of a word.

    This is a wrapper for :py:meth:`SpanishMetaphone.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 6)
    modified : bool
        Set to True to use del Pilar Angeles & Bailón-Miguel's modified version
        of the algorithm

    Returns
    -------
    str
        The Spanish Metaphone code

    Examples
    --------
    >>> spanish_metaphone('Perez')
    'PRZ'
    >>> spanish_metaphone('Martinez')
    'MRTNZ'
    >>> spanish_metaphone('Gutierrez')
    'GTRRZ'
    >>> spanish_metaphone('Santiago')
    'SNTG'
    >>> spanish_metaphone('Nicolás')
    'NKLS'

    """
    return SpanishMetaphone().encode(word, max_length, modified)