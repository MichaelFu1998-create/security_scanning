def dm_soundex(word, max_length=6, zero_pad=True):
    """Return the Daitch-Mokotoff Soundex code for a word.

    This is a wrapper for :py:meth:`DaitchMokotoff.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 6; must be between 6 and
        64)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Daitch-Mokotoff Soundex value

    Examples
    --------
    >>> sorted(dm_soundex('Christopher'))
    ['494379', '594379']
    >>> dm_soundex('Niall')
    {'680000'}
    >>> dm_soundex('Smith')
    {'463000'}
    >>> dm_soundex('Schmidt')
    {'463000'}

    >>> sorted(dm_soundex('The quick brown fox', max_length=20,
    ... zero_pad=False))
    ['35457976754', '3557976754']

    """
    return DaitchMokotoff().encode(word, max_length, zero_pad)