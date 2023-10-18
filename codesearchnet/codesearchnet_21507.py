def replace_macros(tex_source, macros):
    r"""Replace macros in the TeX source with their content.

    Parameters
    ----------
    tex_source : `str`
        TeX source content.
    macros : `dict`
        Keys are macro names (including leading ``\``) and values are the
        content (as `str`) of the macros. See
        `lsstprojectmeta.tex.scraper.get_macros`.

    Returns
    -------
    tex_source : `str`
        TeX source with known macros replaced.

    Notes
    -----
    Macros with arguments are not supported.

    Examples
    --------
    >>> macros = {r'\handle': 'LDM-nnn'}
    >>> sample = r'This is document \handle.'
    >>> replace_macros(sample, macros)
    'This is document LDM-nnn.'

    Any trailing slash after the macro command is also replaced by this
    function.

    >>> macros = {r'\product': 'Data Management'}
    >>> sample = r'\title    [Test Plan]  { \product\ Test Plan}'
    >>> replace_macros(sample, macros)
    '\\title    [Test Plan]  { Data Management Test Plan}'
    """
    for macro_name, macro_content in macros.items():
        # '\\?' suffix matches an optional trailing '\' that might be used
        # for spacing.
        pattern = re.escape(macro_name) + r"\\?"
        # Wrap macro_content in lambda to avoid processing escapes
        tex_source = re.sub(pattern, lambda _: macro_content, tex_source)
    return tex_source