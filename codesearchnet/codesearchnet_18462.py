def get_config(jid):
    """Get the configuration for the given JID based on XMPP_HTTP_UPLOAD_ACCESS.

    If the JID does not match any rule, ``False`` is returned.
    """

    acls = getattr(settings, 'XMPP_HTTP_UPLOAD_ACCESS', (('.*', False), ))

    for regex, config in acls:
        if isinstance(regex, six.string_types):
            regex = [regex]

        for subex in regex:
            if re.search(subex, jid):
                return config

    return False