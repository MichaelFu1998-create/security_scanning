def clickmap(parser, token):
    """
    Clickmap tracker template tag.

    Renders Javascript code to track page visits.  You must supply
    your clickmap tracker ID (as a string) in the ``CLICKMAP_TRACKER_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ClickmapNode()