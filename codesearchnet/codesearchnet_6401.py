def intercom(parser, token):
    """
    Intercom.io template tag.

    Renders Javascript code to intercom.io testing.  You must supply
    your APP ID account number in the ``INTERCOM_APP_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return IntercomNode()