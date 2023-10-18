def resolve_modifier_to_ansi_code(modifiername, colormode):
    """
    Resolve the given modifier name to a valid
    ANSI escape code.

    :param str modifiername: the name of the modifier to resolve
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``

    :returns str: the ANSI escape code for the modifier

    :raises ColorfulError: if the given modifier name is invalid
    """
    if colormode == terminal.NO_COLORS:  # return empty string if colors are disabled
        return '', ''

    try:
        start_code, end_code = ansi.MODIFIERS[modifiername]
    except KeyError:
        raise ColorfulError('the modifier "{0}" is unknown. Use one of: {1}'.format(
            modifiername, ansi.MODIFIERS.keys()))
    else:
        return ansi.ANSI_ESCAPE_CODE.format(
            code=start_code), ansi.ANSI_ESCAPE_CODE.format(
                code=end_code)