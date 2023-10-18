def olark(parser, token):
    """
    Olark set-up template tag.

    Renders Javascript code to set-up Olark chat.  You must supply
    your site ID in the ``OLARK_SITE_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return OlarkNode()