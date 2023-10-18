def hubspot(parser, token):
    """
    HubSpot tracking template tag.

    Renders Javascript code to track page visits.  You must supply
    your portal ID (as a string) in the ``HUBSPOT_PORTAL_ID`` setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return HubSpotNode()