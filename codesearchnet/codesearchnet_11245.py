def lein(word, max_length=4, zero_pad=True):
    """Return the Lein code for a word.

    This is a wrapper for :py:meth:`Lein.encode`.

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
        The Lein code

    Examples
    --------
    >>> lein('Christopher')
    'C351'
    >>> lein('Niall')
    'N300'
    >>> lein('Smith')
    'S210'
    >>> lein('Schmidt')
    'S521'

    """
    return Lein().encode(word, max_length, zero_pad)