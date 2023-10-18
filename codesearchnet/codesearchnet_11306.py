def phonix(word, max_length=4, zero_pad=True):
    """Return the Phonix code for a word.

    This is a wrapper for :py:meth:`Phonix.encode`.

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
        The Phonix value

    Examples
    --------
    >>> phonix('Christopher')
    'K683'
    >>> phonix('Niall')
    'N400'
    >>> phonix('Smith')
    'S530'
    >>> phonix('Schmidt')
    'S530'

    """
    return Phonix().encode(word, max_length, zero_pad)