def _path_root(draw, result_type):
    """Generates a root component for a path."""

    # Based on https://en.wikipedia.org/wiki/Path_(computing)

    def tp(s=''):
        return _str_to_path(s, result_type)

    if os.name != 'nt':
        return tp(os.sep)

    sep = sampled_from([os.sep, os.altsep or os.sep]).map(tp)
    name = _filename(result_type)
    char = characters(min_codepoint=ord("A"), max_codepoint=ord("z")).map(
        lambda c: tp(str(c)))

    relative = sep
    # [drive_letter]:\
    drive = builds(lambda *x: tp().join(x), char, just(tp(':')), sep)
    # \\?\[drive_spec]:\
    extended = builds(
        lambda *x: tp().join(x), sep, sep, just(tp('?')), sep, drive)

    network = one_of([
        # \\[server]\[sharename]\
        builds(lambda *x: tp().join(x), sep, sep, name, sep, name, sep),
        # \\?\[server]\[sharename]\
        builds(lambda *x: tp().join(x),
               sep, sep, just(tp('?')), sep, name, sep, name, sep),
        # \\?\UNC\[server]\[sharename]\
        builds(lambda *x: tp().join(x),
               sep, sep, just(tp('?')), sep, just(tp('UNC')), sep, name, sep,
               name, sep),
        # \\.\[physical_device]\
        builds(lambda *x: tp().join(x),
               sep, sep, just(tp('.')), sep, name, sep),
    ])

    final = one_of(relative, drive, extended, network)

    return draw(final)