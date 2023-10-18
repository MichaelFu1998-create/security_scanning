def get_extenders():
    """
    Retrieves the TidyPy configuration extenders that are available in the
    current Python environment.

    The returned dictionary has keys are the extender names and values are the
    extender classes.

    :rtype: dict
    """

    # pylint: disable=protected-access

    if not hasattr(get_extenders, '_CACHE'):
        get_extenders._CACHE = dict()
        for entry in pkg_resources.iter_entry_points('tidypy.extenders'):
            try:
                get_extenders._CACHE[entry.name] = entry.load()
            except ImportError as exc:  # pragma: no cover
                output_error(
                    'Could not load extender "%s" defined by "%s": %s' % (
                        entry,
                        entry.dist,
                        exc,
                    ),
                )
    return get_extenders._CACHE