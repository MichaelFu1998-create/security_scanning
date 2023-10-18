def soundex_br(word, max_length=4, zero_pad=True):
    """Return the SoundexBR encoding of a word.

    This is a wrapper for :py:meth:`SoundexBR.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The SoundexBR code

    Examples
    --------
    >>> soundex_br('Oliveira')
    'O416'
    >>> soundex_br('Almeida')
    'A453'
    >>> soundex_br('Barbosa')
    'B612'
    >>> soundex_br('Araújo')
    'A620'
    >>> soundex_br('Gonçalves')
    'G524'
    >>> soundex_br('Goncalves')
    'G524'

    """
    return SoundexBR().encode(word, max_length, zero_pad)