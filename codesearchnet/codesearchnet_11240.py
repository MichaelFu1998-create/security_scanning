def roger_root(word, max_length=5, zero_pad=True):
    """Return the Roger Root code for a word.

    This is a wrapper for :py:meth:`RogerRoot.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 5) of the code to return
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Roger Root code

    Examples
    --------
    >>> roger_root('Christopher')
    '06401'
    >>> roger_root('Niall')
    '02500'
    >>> roger_root('Smith')
    '00310'
    >>> roger_root('Schmidt')
    '06310'

    """
    return RogerRoot().encode(word, max_length, zero_pad)