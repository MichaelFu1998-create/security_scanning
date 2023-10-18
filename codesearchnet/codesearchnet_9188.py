def style_string(string, ansi_style, colormode, nested=False):
    """
    Style the given string according to the given
    ANSI style string.

    :param str string: the string to style
    :param tuple ansi_style: the styling string returned by ``translate_style``
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``

    :returns: a string containing proper ANSI sequence
    """
    ansi_start_code, ansi_end_code = ansi_style

    # replace nest placeholders with the current begin style
    if PY2:
        if isinstance(string, str):
            string = string.decode(DEFAULT_ENCODING)
    string = UNICODE(string).replace(ansi.NEST_PLACEHOLDER, ansi_start_code)

    return '{start_code}{string}{end_code}{nest_ph}'.format(
            start_code=ansi_start_code,
            string=string,
            end_code=ansi_end_code,
            nest_ph=ansi.NEST_PLACEHOLDER if nested else '')