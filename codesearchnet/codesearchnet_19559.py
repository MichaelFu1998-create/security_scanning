def named(typename, *fieldnames, **defaults):
    """
    namedtuple with default values
    named('typename', fields | *fields, default=x, [**defaults])
    :param typename:
    :param fieldnames:
    :param defaults:
    :return:
    """
    if len(fieldnames) == 1:
        if isinstance(fieldnames[0], str):
            fieldnames = tuple(fieldnames[0].replace(',', ' ').split())
        elif isinstance(fieldnames[0], (list, tuple)):
            fieldnames = fieldnames[0]

    # set default of defaults
    default_of_defaults = defaults.pop('default', None)

    dfields = tuple(f for f in defaults if f not in fieldnames)

    T = collections.namedtuple(typename, fieldnames + dfields)
    T.__new__.__defaults__ = (default_of_defaults,) * len(T._fields)
    prototype = T(**defaults)
    T.__new__.__defaults__ = tuple(prototype)

    # make picklable
    globals()[typename] = T

    return T