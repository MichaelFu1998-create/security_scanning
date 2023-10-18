def pshp_soundex_last(lname, max_length=4, german=False):
    """Calculate the PSHP Soundex/Viewex Coding of a last name.

    This is a wrapper for :py:meth:`PSHPSoundexLast.encode`.

    Parameters
    ----------
    lname : str
        The last name to encode
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
    >>> pshp_soundex_last('Smith')
    'S530'
    >>> pshp_soundex_last('Waters')
    'W350'
    >>> pshp_soundex_last('James')
    'J500'
    >>> pshp_soundex_last('Schmidt')
    'S530'
    >>> pshp_soundex_last('Ashcroft')
    'A225'

    """
    return PSHPSoundexLast().encode(lname, max_length, german)