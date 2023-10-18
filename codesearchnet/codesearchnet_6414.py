def gauges(parser, token):
    """
    Gaug.es template tag.

    Renders Javascript code to gaug.es testing.  You must supply
    your Site ID account number in the ``GAUGES_SITE_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return GaugesNode()