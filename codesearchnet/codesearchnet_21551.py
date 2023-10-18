def get_newcommand_macros(tex_source):
    r"""Get all ``\newcommand`` macro definition from TeX source.

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
    ``\newcommand`` macros with arguments are not supported.
    """
    macros = {}
    command = LatexCommand(
        'newcommand',
        {'name': 'name', 'required': True, 'bracket': '{'},
        {'name': 'content', 'required': True, 'bracket': '{'})

    for macro in command.parse(tex_source):
        macros[macro['name']] = macro['content']

    return macros