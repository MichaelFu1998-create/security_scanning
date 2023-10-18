def kiss_metrics(parser, token):
    """
    KISSinsights tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your KISSmetrics API key in the ``KISS_METRICS_API_KEY``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return KissMetricsNode()