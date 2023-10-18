def _HandleContentsEol(contents, eol_style):
    '''
    Replaces eol on each line by the given eol_style.

    :param unicode contents:
    :type eol_style: EOL_STYLE_XXX constant
    :param eol_style:
    '''
    if eol_style == EOL_STYLE_NONE:
        return contents

    if eol_style == EOL_STYLE_UNIX:
        return contents.replace('\r\n', eol_style).replace('\r', eol_style)

    if eol_style == EOL_STYLE_MAC:
        return contents.replace('\r\n', eol_style).replace('\n', eol_style)

    if eol_style == EOL_STYLE_WINDOWS:
        return contents.replace('\r\n', '\n').replace('\r', '\n').replace('\n', EOL_STYLE_WINDOWS)

    raise ValueError('Unexpected eol style: %r' % (eol_style,))