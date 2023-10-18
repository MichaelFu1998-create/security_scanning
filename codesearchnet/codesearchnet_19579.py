def run(main=None, argv=None, **flags):
    """
    :param main: main or sys.modules['__main__'].main
    :param argv: argument list used in argument parse
    :param flags: flags to define with defaults
    :return:
    """
    """Runs the program with an optional 'main' function and 'argv' list."""
    import sys as _sys
    import inspect
    main = main or _sys.modules['__main__'].main

    if main.__doc__:
        docstring = main.__doc__.split(':param')[0]
        _parser.usage = 'from docstring \n {}'.format(docstring)  # add_help

    # if not flags:
    try:
        a = inspect.getfullargspec(main)
    except AttributeError:
        a = inspect.getargspec(main)  # namedtuple(args, varargs, keywords, defaults)
    if a.defaults:
        kwargs = dict(zip(reversed(a.args), reversed(a.defaults)))
        add_flag(**kwargs)
    else:
        kwargs = dict()

    # add to command argument
    if a.defaults is None:
        nargs = len(a.args)
    else:
        nargs = len(a.args) - len(a.defaults)
    # if nargs > 0:
    posargs = a.args[:nargs]
    flag.add_args(posargs)
    add_flag(**flags)

    # Extract the args from the optional `argv` list.
    args = argv[1:] if argv else None

    # Parse the known flags from that list, or from the command
    # line otherwise.
    unparsed, kw = flag._parse_flags_kw(args=args)

    d = flag.__dict__['__flags']
    args = [d[k] for k in posargs]
    args += unparsed

    kwargs.update({k: d[k] for k in kwargs.keys()})
    kwargs.update(kw)

    # Call the main function, passing through any arguments,
    # with parsed flags as kwwargs
    # to the final program.
    _sys.exit(main(*args, **kwargs))