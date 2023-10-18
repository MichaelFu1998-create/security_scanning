def translate_style(style, colormode, colorpalette):
    """
    Translate the given style to an ANSI escape code
    sequence.

    ``style`` examples are:

    * green
    * bold
    * red_on_black
    * bold_green
    * italic_yellow_on_cyan

    :param str style: the style to translate
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
    :parma dict colorpalette: the color palette to use for the color name mapping
    """
    style_parts = iter(style.split('_'))

    ansi_start_sequence = []
    ansi_end_sequence = []

    try:
        # consume all modifiers
        part = None
        for mod_part in style_parts:
            part = mod_part
            if part not in ansi.MODIFIERS:
                break  # all modifiers have been consumed

            mod_start_code, mod_end_code = resolve_modifier_to_ansi_code(part, colormode)
            ansi_start_sequence.append(mod_start_code)
            ansi_end_sequence.append(mod_end_code)
        else:  # we've consumed all parts, thus we can exit
            raise StopIteration()

        # next part has to be a foreground color or the 'on' keyword
        # which means we have to consume background colors
        if part != 'on':
            ansi_start_code, ansi_end_code = translate_colorname_to_ansi_code(
                part, ansi.FOREGROUND_COLOR_OFFSET, colormode, colorpalette)
            ansi_start_sequence.append(ansi_start_code)
            ansi_end_sequence.append(ansi_end_code)
            # consume the required 'on' keyword after the foreground color
            next(style_parts)

        # next part has to be the background color
        part = next(style_parts)
        ansi_start_code, ansi_end_code = translate_colorname_to_ansi_code(
            part, ansi.BACKGROUND_COLOR_OFFSET, colormode, colorpalette)
        ansi_start_sequence.append(ansi_start_code)
        ansi_end_sequence.append(ansi_end_code)
    except StopIteration:  # we've consumed all parts of the styling string
        pass

    # construct and return ANSI escape code sequence
    return ''.join(ansi_start_sequence), ''.join(ansi_end_sequence)