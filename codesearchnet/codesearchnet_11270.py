def pshp_soundex_first(fname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a first name.

    This is a wrapper for :py:meth:`PSHPSoundexFirst.encode`.

    Parameters
    ----------
    fname : str
        The first name to encode
    max_length : int
        The length of the code returned (defaults to 4)
    german : bool
        Set to True if the name is German (different rules apply)

    Returns
    -------
    str
        The PSHP Soundex/Viewex Coding

    Examples
    --------
    >>> pshp_soundex_first('Smith')
    'S530'
    >>> pshp_soundex_first('Waters')
    'W352'
    >>> pshp_soundex_first('James')
    'J700'
    >>> pshp_soundex_first('Schmidt')
    'S500'
    >>> pshp_soundex_first('Ashcroft')
    'A220'
    >>> pshp_soundex_first('John')
    'J500'
    >>> pshp_soundex_first('Colin')
    'K400'
    >>> pshp_soundex_first('Niall')
    'N400'
    >>> pshp_soundex_first('Sally')
    'S400'
    >>> pshp_soundex_first('Jane')
    'J500'

    """
    return PSHPSoundexFirst().encode(fname, max_length, german)