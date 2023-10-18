def optimizely(parser, token):
    """
    Optimizely template tag.

    Renders Javascript code to set-up A/B testing.  You must supply
    your Optimizely account number in the ``OPTIMIZELY_ACCOUNT_NUMBER``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return OptimizelyNode()