def phonex(word, max_length=4, zero_pad=True):
    """Return the Phonex code for a word.

    This is a wrapper for :py:meth:`Phonex.encode`.

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
        The Phonex value

    Examples
    --------
    >>> phonex('Christopher')
    'C623'
    >>> phonex('Niall')
    'N400'
    >>> phonex('Schmidt')
    'S253'
    >>> phonex('Smith')
    'S530'

    """
    return Phonex().encode(word, max_length, zero_pad)