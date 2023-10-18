def refined_soundex(word, max_length=-1, zero_pad=False, retain_vowels=False):
    """Return the Refined Soundex code for a word.

    This is a wrapper for :py:meth:`RefinedSoundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to unlimited)
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string
    retain_vowels : bool
        Retain vowels (as 0) in the resulting code

    Returns
    -------
    str
        The Refined Soundex value

    Examples
    --------
    >>> refined_soundex('Christopher')
    'C393619'
    >>> refined_soundex('Niall')
    'N87'
    >>> refined_soundex('Smith')
    'S386'
    >>> refined_soundex('Schmidt')
    'S386'

    """
    return RefinedSoundex().encode(word, max_length, zero_pad, retain_vowels)