def gosquared(parser, token):
    """
    GoSquared tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your GoSquared site token in the ``GOSQUARED_SITE_TOKEN`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GoSquaredNode()