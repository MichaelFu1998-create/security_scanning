def chartbeat_top(parser, token):
    """
    Top Chartbeat template tag.

    Render the top Javascript code for Chartbeat.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ChartbeatTopNode()