def crazy_egg(parser, token):
    """
    Crazy Egg tracking template tag.

    Renders Javascript code to track page clicks.  You must supply
    your Crazy Egg account number (as a string) in the
    ``CRAZY_EGG_ACCOUNT_NUMBER`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return CrazyEggNode()