def qgram_fingerprint(phrase, qval=2, start_stop='', joiner=''):
    """Return Q-Gram fingerprint.

    This is a wrapper for :py:meth:`QGram.fingerprint`.

    Parameters
    ----------
    phrase : str
        The string from which to calculate the q-gram fingerprint
    qval : int
        The length of each q-gram (by default 2)
    start_stop : str
        The start & stop symbol(s) to concatenate on either end of the phrase,
        as defined in :py:class:`tokenizer.QGrams`
    joiner : str
        The string that will be placed between each word

    Returns
    -------
    str
        The q-gram fingerprint of the phrase

    Examples
    --------
    >>> qgram_fingerprint('The quick brown fox jumped over the lazy dog.')
    'azbrckdoedeleqerfoheicjukblampnfogovowoxpequrortthuiumvewnxjydzy'
    >>> qgram_fingerprint('Christopher')
    'cherhehrisopphristto'
    >>> qgram_fingerprint('Niall')
    'aliallni'

    """
    return QGram().fingerprint(phrase, qval, start_stop, joiner)