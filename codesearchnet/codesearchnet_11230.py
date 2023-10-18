def synoname_toolcode(lname, fname='', qual='', normalize=0):
    """Build the Synoname toolcode.

    This is a wrapper for :py:meth:`SynonameToolcode.fingerprint`.

    Parameters
    ----------
    lname : str
        Last name
    fname : str
        First name (can be blank)
    qual : str
        Qualifier
    normalize : int
        Normalization mode (0, 1, or 2)

    Returns
    -------
    tuple
        The transformed names and the synoname toolcode

    Examples
    --------
    >>> synoname_toolcode('hat')
    ('hat', '', '0000000003$$h')
    >>> synoname_toolcode('niall')
    ('niall', '', '0000000005$$n')
    >>> synoname_toolcode('colin')
    ('colin', '', '0000000005$$c')
    >>> synoname_toolcode('atcg')
    ('atcg', '', '0000000004$$a')
    >>> synoname_toolcode('entreatment')
    ('entreatment', '', '0000000011$$e')

    >>> synoname_toolcode('Ste.-Marie', 'Count John II', normalize=2)
    ('ste.-marie ii', 'count john', '0200491310$015b049a127c$smcji')
    >>> synoname_toolcode('Michelangelo IV', '', 'Workshop of')
    ('michelangelo iv', '', '3000550015$055b$mi')

    """
    return SynonameToolcode().fingerprint(lname, fname, qual, normalize)