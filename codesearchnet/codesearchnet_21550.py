def get_def_macros(tex_source):
    r"""Get all ``\def`` macro definition from TeX source.

    Parameters
    ----------
    tex_source : `str`
        TeX source content.

    Returns
    -------
    macros : `dict`
        Keys are macro names (including leading ``\``) and values are the
        content (as `str`) of the macros.

    Notes
    -----
    ``\def`` macros with arguments are not supported.
    """
    macros = {}
    for match in DEF_PATTERN.finditer(tex_source):
        macros[match.group('name')] = match.group('content')
    return macros