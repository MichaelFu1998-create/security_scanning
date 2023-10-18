def __prepare_resource(data):
        """Prepare the resourcepart of the JID.

        :Parameters:
            - `data`: Resourcepart of the JID

        :raise JIDError: if the resource name is too long.
        :raise pyxmpp.xmppstringprep.StringprepError: if the
            resourcepart fails Resourceprep preparation."""
        if not data:
            return None
        data = unicode(data)
        try:
            resource = RESOURCEPREP.prepare(data)
        except StringprepError, err:
            raise JIDError(u"Local part invalid: {0}".format(err))
        if len(resource.encode("utf-8")) > 1023:
            raise JIDError("Resource name too long")
        return resource