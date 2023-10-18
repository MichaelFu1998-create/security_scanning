def kiss_insights(parser, token):
    """
    KISSinsights set-up template tag.

    Renders Javascript code to set-up surveys.  You must supply
    your account number and site code in the
    ``KISS_INSIGHTS_ACCOUNT_NUMBER`` and ``KISS_INSIGHTS_SITE_CODE``
    settings.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return KissInsightsNode()