def sim_typo(
    src, tar, metric='euclidean', cost=(1, 1, 0.5, 0.5), layout='QWERTY'
):
    """Return the normalized typo similarity between two strings.

    This is a wrapper for :py:meth:`Typo.sim`.

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
        Normalized typo similarity

    Examples
    --------
    >>> round(sim_typo('cat', 'hat'), 12)
    0.472953716914
    >>> round(sim_typo('Niall', 'Neil'), 12)
    0.434971857071
    >>> round(sim_typo('Colin', 'Cuilen'), 12)
    0.430964390437
    >>> sim_typo('ATCG', 'TAGC')
    0.375

    """
    return Typo().sim(src, tar, metric, cost, layout)