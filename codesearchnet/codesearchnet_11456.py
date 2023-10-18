def get_tools():
    """
    Retrieves the TidyPy tools that are available in the current Python
    environment.

    The returned dictionary has keys that are the tool names and values are the
    tool classes.

    :rtype: dict
    """

    # pylint: disable=protected-access

    if not hasattr(get_tools, '_CACHE'):
        get_tools._CACHE = dict()
        for entry in pkg_resources.iter_entry_points('tidypy.tools'):
            try:
                get_tools._CACHE[entry.name] = entry.load()
            except ImportError as exc:  # pragma: no cover
                output_error(
                    'Could not load tool "%s" defined by "%s": %s' % (
                        entry,
                        entry.dist,
                        exc,
                    ),
                )
    return get_tools._CACHE