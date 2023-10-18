def dolby(word, max_length=-1, keep_vowels=False, vowel_char='*'):
    r"""Return the Dolby Code of a name.

    This is a wrapper for :py:meth:`Dolby.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        Maximum length of the returned Dolby code -- this also activates the
        fixed-length code mode if it is greater than 0
    keep_vowels : bool
        If True, retains all vowel markers
    vowel_char : str
        The vowel marker character (default to \*)

    Returns
    -------
    str
        The Dolby Code

    Examples
    --------
    >>> dolby('Hansen')
    'H*NSN'
    >>> dolby('Larsen')
    'L*RSN'
    >>> dolby('Aagaard')
    '*GR'
    >>> dolby('Braaten')
    'BR*DN'
    >>> dolby('Sandvik')
    'S*NVK'
    >>> dolby('Hansen', max_length=6)
    'H*NS*N'
    >>> dolby('Larsen', max_length=6)
    'L*RS*N'
    >>> dolby('Aagaard', max_length=6)
    '*G*R  '
    >>> dolby('Braaten', max_length=6)
    'BR*D*N'
    >>> dolby('Sandvik', max_length=6)
    'S*NF*K'

    >>> dolby('Smith')
    'SM*D'
    >>> dolby('Waters')
    'W*DRS'
    >>> dolby('James')
    'J*MS'
    >>> dolby('Schmidt')
    'SM*D'
    >>> dolby('Ashcroft')
    '*SKRFD'
    >>> dolby('Smith', max_length=6)
    'SM*D  '
    >>> dolby('Waters', max_length=6)
    'W*D*RS'
    >>> dolby('James', max_length=6)
    'J*M*S '
    >>> dolby('Schmidt', max_length=6)
    'SM*D  '
    >>> dolby('Ashcroft', max_length=6)
    '*SKRFD'

    """
    return Dolby().encode(word, max_length, keep_vowels, vowel_char)