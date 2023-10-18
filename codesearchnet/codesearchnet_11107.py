def davidson(lname, fname='.', omit_fname=False):
    """Return Davidson's Consonant Code.

    This is a wrapper for :py:meth:`Davidson.encode`.

    Parameters
    ----------
    lname : str
        Last name (or word) to be encoded
    fname : str
        First name (optional), of which the first character is included in the
        code.
    omit_fname : bool
        Set to True to completely omit the first character of the first name

    Returns
    -------
    str
        Davidson's Consonant Code

    Example
    -------
    >>> davidson('Gough')
    'G   .'
    >>> davidson('pneuma')
    'PNM .'
    >>> davidson('knight')
    'KNGT.'
    >>> davidson('trice')
    'TRC .'
    >>> davidson('judge')
    'JDG .'
    >>> davidson('Smith', 'James')
    'SMT J'
    >>> davidson('Wasserman', 'Tabitha')
    'WSRMT'

    """
    return Davidson().encode(lname, fname, omit_fname)