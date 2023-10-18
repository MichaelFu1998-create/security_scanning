def uealite(
    word,
    max_word_length=20,
    max_acro_length=8,
    return_rule_no=False,
    var='standard',
):
    """Return UEA-Lite stem.

    This is a wrapper for :py:meth:`UEALite.stem`.

    Parameters
    ----------
    word : str
        The word to stem
    max_word_length : int
        The maximum word length allowed
    max_acro_length : int
        The maximum acronym length allowed
    return_rule_no : bool
        If True, returns the stem along with rule number
    var : str
        Variant rules to use:

            - ``Adams`` to use Jason Adams' rules
            - ``Perl`` to use the original Perl rules

    Returns
    -------
    str or (str, int)
        Word stem

    Examples
    --------
    >>> uealite('readings')
    'read'
    >>> uealite('insulted')
    'insult'
    >>> uealite('cussed')
    'cuss'
    >>> uealite('fancies')
    'fancy'
    >>> uealite('eroded')
    'erode'

    """
    return UEALite().stem(
        word, max_word_length, max_acro_length, return_rule_no, var
    )