def performable(parser, token):
    """
    Performable template tag.

    Renders Javascript code to set-up Performable tracking.  You must
    supply your Performable API key in the ``PERFORMABLE_API_KEY``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return PerformableNode()