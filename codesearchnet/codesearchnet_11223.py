def nysiis(word, max_length=6, modified=False):
    """Return the NYSIIS code for a word.

    This is a wrapper for :py:meth:`NYSIIS.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The maximum length (default 6) of the code to return
    modified : bool
        Indicates whether to use USDA modified NYSIIS

    Returns
    -------
    str
        The NYSIIS value

    Examples
    --------
    >>> nysiis('Christopher')
    'CRASTA'
    >>> nysiis('Niall')
    'NAL'
    >>> nysiis('Smith')
    'SNAT'
    >>> nysiis('Schmidt')
    'SNAD'

    >>> nysiis('Christopher', max_length=-1)
    'CRASTAFAR'

    >>> nysiis('Christopher', max_length=8, modified=True)
    'CRASTAFA'
    >>> nysiis('Niall', max_length=8, modified=True)
    'NAL'
    >>> nysiis('Smith', max_length=8, modified=True)
    'SNAT'
    >>> nysiis('Schmidt', max_length=8, modified=True)
    'SNAD'

    """
    return NYSIIS().encode(word, max_length, modified)