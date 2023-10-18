def filter_gromacs_warnings(action, categories=None):
    """Set the :meth:`warnings.simplefilter` to *action*.

    *categories* must be a list of warning classes or strings.
    ``None`` selects the defaults,  :data:`gromacs.less_important_warnings`.
    """

    if categories is None:
        categories = less_important_warnings
    for c in categories:
        try:
            w = globals()[c]
        except KeyError:
            w = c
        if not issubclass(w, Warning):
            raise TypeError("{0!r} is neither a Warning nor the name of a Gromacs warning.".format(c))
        warnings.simplefilter(action, category=w)