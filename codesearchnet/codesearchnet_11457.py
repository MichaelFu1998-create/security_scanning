def get_reports():
    """
    Retrieves the TidyPy issue reports that are available in the current Python
    environment.

    The returned dictionary has keys are the report names and values are the
    report classes.

    :rtype: dict
    """

    # pylint: disable=protected-access

    if not hasattr(get_reports, '_CACHE'):
        get_reports._CACHE = dict()
        for entry in pkg_resources.iter_entry_points('tidypy.reports'):
            try:
                get_reports._CACHE[entry.name] = entry.load()
            except ImportError as exc:  # pragma: no cover
                output_error(
                    'Could not load report "%s" defined by "%s": %s' % (
                        entry,
                        entry.dist,
                        exc,
                    ),
                )
    return get_reports._CACHE