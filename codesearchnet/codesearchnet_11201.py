def typo(src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'):
    """Return the typo distance between two strings.

    This is a wrapper for :py:meth:`Typo.typo`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    metric : str
        Supported values include: ``euclidean``, ``manhattan``,
        ``log-euclidean``, and ``log-manhattan``
    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and shift, respectively (by default:
        (1, 1, 0.5, 0.5)) The substitution & shift costs should be
        significantly less than the cost of an insertion & deletion unless a
        log metric is used.
    layout : str
        Name of the keyboard layout to use (Currently supported:
        ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

    Returns
    -------
    float
        Typo distance

    Examples
    --------
    >>> typo('cat', 'hat')
    1.5811388
    >>> typo('Niall', 'Neil')
    2.8251407
    >>> typo('Colin', 'Cuilen')
    3.4142137
    >>> typo('ATCG', 'TAGC')
    2.5

    >>> typo('cat', 'hat', metric='manhattan')
    2.0
    >>> typo('Niall', 'Neil', metric='manhattan')
    3.0
    >>> typo('Colin', 'Cuilen', metric='manhattan')
    3.5
    >>> typo('ATCG', 'TAGC', metric='manhattan')
    2.5

    >>> typo('cat', 'hat', metric='log-manhattan')
    0.804719
    >>> typo('Niall', 'Neil', metric='log-manhattan')
    2.2424533
    >>> typo('Colin', 'Cuilen', metric='log-manhattan')
    2.2424533
    >>> typo('ATCG', 'TAGC', metric='log-manhattan')
    2.3465736

    """
    return Typo().dist_abs(src, tar, metric, cost, layout)