def rating_mailru(parser, token):
    """
    Rating@Mail.ru counter template tag.

    Renders Javascript code to track page visits. You must supply
    your website counter ID (as a string) in the
    ``RATING_MAILRU_COUNTER_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return RatingMailruNode()