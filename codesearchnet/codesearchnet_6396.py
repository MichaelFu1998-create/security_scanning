def snapengage(parser, token):
    """
    SnapEngage set-up template tag.

    Renders Javascript code to set-up SnapEngage chat.  You must supply
    your widget ID in the ``SNAPENGAGE_WIDGET_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return SnapEngageNode()