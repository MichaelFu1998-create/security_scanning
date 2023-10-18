def fspaths(draw, allow_pathlike=None):
    """A strategy which generates filesystem path values.

    The generated values include everything which the builtin
    :func:`python:open` function accepts i.e. which won't lead to
    :exc:`ValueError` or :exc:`TypeError` being raised.

    Note that the range of the returned values depends on the operating
    system, the Python version, and the filesystem encoding as returned by
    :func:`sys.getfilesystemencoding`.

    :param allow_pathlike:
        If :obj:`python:None` makes the strategy include objects implementing
        the :class:`python:os.PathLike` interface when Python >= 3.6 is used.
        If :obj:`python:False` no pathlike objects will be generated. If
        :obj:`python:True` pathlike will be generated (Python >= 3.6 required)

    :type allow_pathlike: :obj:`python:bool` or :obj:`python:None`

    .. versionadded:: 3.15

    """
    has_pathlike = hasattr(os, 'PathLike')

    if allow_pathlike is None:
        allow_pathlike = has_pathlike
    if allow_pathlike and not has_pathlike:
        raise InvalidArgument(
            'allow_pathlike: os.PathLike not supported, use None instead '
            'to enable it only when available')

    result_type = draw(sampled_from([bytes, text_type]))

    def tp(s=''):
        return _str_to_path(s, result_type)

    special_component = sampled_from([tp(os.curdir), tp(os.pardir)])
    normal_component = _filename(result_type)
    path_component = one_of(normal_component, special_component)
    extension = normal_component.map(lambda f: tp(os.extsep) + f)
    root = _path_root(result_type)

    def optional(st):
        return one_of(st, just(result_type()))

    sep = sampled_from([os.sep, os.altsep or os.sep]).map(tp)
    path_part = builds(lambda s, l: s.join(l), sep, lists(path_component))
    main_strategy = builds(lambda *x: tp().join(x),
                           optional(root), path_part, optional(extension))

    if allow_pathlike and hasattr(os, 'fspath'):
        pathlike_strategy = main_strategy.map(lambda p: _PathLike(p))
        main_strategy = one_of(main_strategy, pathlike_strategy)

    return draw(main_strategy)