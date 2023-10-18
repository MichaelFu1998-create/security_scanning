def _check_authorization(self, properties, stream):
        """Check authorization id and other properties returned by the
        authentication mechanism.

        [receiving entity only]

        Allow only no authzid or authzid equal to current username@domain

        FIXME: other rules in s2s

        :Parameters:
            - `properties`: data obtained during authentication
        :Types:
            - `properties`: mapping

        :return: `True` if user is authorized to use a provided authzid
        :returntype: `bool`
        """
        authzid = properties.get("authzid")
        if not authzid:
            return True
        try:
            jid = JID(authzid)
        except ValueError:
            return False

        if "username" not in properties:
            result = False
        elif jid.local != properties["username"]:
            result = False
        elif jid.domain != stream.me.domain:
            result = False
        elif jid.resource:
            result = False
        else:
            result = True
        return result