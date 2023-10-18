def get_macros(tex_source):
    r"""Get all macro definitions from TeX source, supporting multiple
    declaration patterns.

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
    This function uses the following function to scrape macros of different
    types:

    - `get_def_macros`
    - `get_newcommand_macros`

    This macro scraping has the following caveats:

    - Macro definition (including content) must all occur on one line.
    - Macros with arguments are not supported.
    """
    macros = {}
    macros.update(get_def_macros(tex_source))
    macros.update(get_newcommand_macros(tex_source))
    return macros