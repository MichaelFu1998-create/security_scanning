def __prepare_local(data):
        """Prepare localpart of the JID

        :Parameters:
            - `data`: localpart of the JID
        :Types:
            - `data`: `unicode`

        :raise JIDError: if the local name is too long.
        :raise pyxmpp.xmppstringprep.StringprepError: if the
            local name fails Nodeprep preparation."""
        if not data:
            return None
        data = unicode(data)
        try:
            local = NODEPREP.prepare(data)
        except StringprepError, err:
            raise JIDError(u"Local part invalid: {0}".format(err))
        if len(local.encode("utf-8")) > 1023:
            raise JIDError(u"Local part too long")
        return local