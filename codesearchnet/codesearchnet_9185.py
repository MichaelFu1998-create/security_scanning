def translate_colorname_to_ansi_code(colorname, offset, colormode, colorpalette):
    """
    Translate the given color name to a valid
    ANSI escape code.

    :parma str colorname: the name of the color to resolve
    :parma str offset: the offset for the color code
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
    :parma dict colorpalette: the color palette to use for the color name mapping

    :returns str: the color as ANSI escape code

    :raises ColorfulError: if the given color name is invalid
    """
    try:
        red, green, blue = colorpalette[colorname]
    except KeyError:
        raise ColorfulError('the color "{0}" is unknown. Use a color in your color palette (by default: X11 rgb.txt)'.format(  # noqa
            colorname))
    else:
        return translate_rgb_to_ansi_code(red, green, blue, offset, colormode)