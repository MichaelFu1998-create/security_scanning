def echo_via_pager(text, color=None):
    """This function takes a text and shows it via an environment specific
    pager on stdout.

    .. versionchanged:: 3.0
       Added the `color` flag.

    :param text: the text to page.
    :param color: controls if the pager supports ANSI colors or not.  The
                  default is autodetection.
    """
    color = resolve_color_default(color)
    if not isinstance(text, string_types):
        text = text_type(text)
    from ._termui_impl import pager
    return pager(text + '\n', color)