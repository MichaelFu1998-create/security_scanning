def synoname(
    src,
    tar,
    word_approx_min=0.3,
    char_approx_min=0.73,
    tests=2 ** 12 - 1,
    ret_name=False,
):
    """Return the Synoname similarity type of two words.

    This is a wrapper for :py:meth:`Synoname.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    word_approx_min : float
        The minimum word approximation value to signal a 'word_approx' match
    char_approx_min : float
        The minimum character approximation value to signal a 'char_approx'
        match
    tests : int or Iterable
        Either an integer indicating tests to perform or a list of test names
        to perform (defaults to performing all tests)
    ret_name : bool
        If True, returns the match name rather than its integer equivalent

    Returns
    -------
    int (or str if ret_name is True)
        Synoname value

    Examples
    --------
    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''))
    2
    >>> synoname(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''),
    ... ret_name=True)
    'omission'
    >>> synoname(('Dore', 'Gustave', ''),
    ... ('Dore', 'Paul Gustave Louis Christophe', ''), ret_name=True)
    'inclusion'
    >>> synoname(('Pereira', 'I. R.', ''), ('Pereira', 'I. Smith', ''),
    ... ret_name=True)
    'word_approx'

    """
    return Synoname().dist_abs(
        src, tar, word_approx_min, char_approx_min, tests, ret_name
    )