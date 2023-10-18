def translate_rgb_to_ansi_code(red, green, blue, offset, colormode):
    """
    Translate the given RGB color into the appropriate ANSI escape code
    for the given color mode.
    The offset is used for the base color which is used.

    The ``colormode`` has to be one of:
        * 0: no colors / disabled
        * 8: use ANSI 8 colors
        * 16: use ANSI 16 colors (same as 8 but with brightness)
        * 256: use ANSI 256 colors
        * 0xFFFFFF / 16777215: use 16 Million true colors

    :param int red: the red channel value
    :param int green: the green channel value
    :param int blue: the blue channel value
    :param int offset: the offset to use for the base color
    :param int colormode: the color mode to use. See explanation above
    """
    if colormode == terminal.NO_COLORS:  # colors are disabled, thus return empty string
        return '', ''

    if colormode == terminal.ANSI_8_COLORS or colormode == terminal.ANSI_16_COLORS:
        color_code = ansi.rgb_to_ansi16(red, green, blue)
        start_code = ansi.ANSI_ESCAPE_CODE.format(
            code=color_code + offset - ansi.FOREGROUND_COLOR_OFFSET)
        end_code = ansi.ANSI_ESCAPE_CODE.format(code=offset + ansi.COLOR_CLOSE_OFFSET)
        return start_code, end_code

    if colormode == terminal.ANSI_256_COLORS:
        color_code = ansi.rgb_to_ansi256(red, green, blue)
        start_code = ansi.ANSI_ESCAPE_CODE.format(code='{base};5;{code}'.format(
            base=8 + offset, code=color_code))
        end_code = ansi.ANSI_ESCAPE_CODE.format(code=offset + ansi.COLOR_CLOSE_OFFSET)
        return start_code, end_code

    if colormode == terminal.TRUE_COLORS:
        start_code = ansi.ANSI_ESCAPE_CODE.format(code='{base};2;{red};{green};{blue}'.format(
            base=8 + offset, red=red, green=green, blue=blue))
        end_code = ansi.ANSI_ESCAPE_CODE.format(code=offset + ansi.COLOR_CLOSE_OFFSET)
        return start_code, end_code

    raise ColorfulError('invalid color mode "{0}"'.format(colormode))