def soundex(word, max_length=4, var='American', reverse=False, zero_pad=True):
    """Return the Soundex code for a word.

    This is a wrapper for :py:meth:`Soundex.encode`.

    Parameters
    ----------
    word : str
        The word to transform
    max_length : int
        The length of the code returned (defaults to 4)
    var : str
        The variant of the algorithm to employ (defaults to ``American``):

            - ``American`` follows the American Soundex algorithm, as described
              at :cite:`US:2007` and in :cite:`Knuth:1998`; this is also called
              Miracode
            - ``special`` follows the rules from the 1880-1910 US Census
              retrospective re-analysis, in which h & w are not treated as
              blocking consonants but as vowels. Cf. :cite:`Repici:2013`.
            - ``Census`` follows the rules laid out in GIL 55 :cite:`US:1997`
              by the US Census, including coding prefixed and unprefixed
              versions of some names

    reverse : bool
        Reverse the word before computing the selected Soundex (defaults to
        False); This results in "Reverse Soundex", which is useful for blocking
        in cases where the initial elements may be in error.
    zero_pad : bool
        Pad the end of the return value with 0s to achieve a max_length string

    Returns
    -------
    str
        The Soundex value

    Examples
    --------
    >>> soundex("Christopher")
    'C623'
    >>> soundex("Niall")
    'N400'
    >>> soundex('Smith')
    'S530'
    >>> soundex('Schmidt')
    'S530'

    >>> soundex('Christopher', max_length=-1)
    'C623160000000000000000000000000000000000000000000000000000000000'
    >>> soundex('Christopher', max_length=-1, zero_pad=False)
    'C62316'

    >>> soundex('Christopher', reverse=True)
    'R132'

    >>> soundex('Ashcroft')
    'A261'
    >>> soundex('Asicroft')
    'A226'
    >>> soundex('Ashcroft', var='special')
    'A226'
    >>> soundex('Asicroft', var='special')
    'A226'

    """
    return Soundex().encode(word, max_length, var, reverse, zero_pad)