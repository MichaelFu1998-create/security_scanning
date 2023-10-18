def chartbeat_bottom(parser, token):
    """
    Bottom Chartbeat template tag.

    Render the bottom Javascript code for Chartbeat.  You must supply
    your Chartbeat User ID (as a string) in the ``CHARTBEAT_USER_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ChartbeatBottomNode()