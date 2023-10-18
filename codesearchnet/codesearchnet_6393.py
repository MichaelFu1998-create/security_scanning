def spring_metrics(parser, token):
    """
    Spring Metrics tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Spring Metrics Tracking ID in the
    ``SPRING_METRICS_TRACKING_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return SpringMetricsNode()