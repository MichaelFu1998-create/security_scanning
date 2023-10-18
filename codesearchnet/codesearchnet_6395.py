def matomo(parser, token):
    """
    Matomo tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your Matomo domain (plus optional URI path), and tracked site ID
    in the ``MATOMO_DOMAIN_PATH`` and the ``MATOMO_SITE_ID`` setting.

    Custom variables can be passed in the ``matomo_vars`` context
    variable.  It is an iterable of custom variables as tuples like:
    ``(index, name, value[, scope])`` where scope may be ``'page'``
    (default) or ``'visit'``.  Index should be an integer and the
    other parameters should be strings.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return MatomoNode()