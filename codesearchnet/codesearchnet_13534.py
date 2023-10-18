def set_payload(self, payload):
        """Set stanza payload to a single item.

        All current stanza content of will be dropped.
        Marks the stanza dirty.

        :Parameters:
            - `payload`: XML element or stanza payload object to use
        :Types:
            - `payload`: :etree:`ElementTree.Element` or `StanzaPayload`
        """
        if isinstance(payload, ElementClass):
            self._payload = [ XMLPayload(payload) ]
        elif isinstance(payload, StanzaPayload):
            self._payload = [ payload ]
        else:
            raise TypeError("Bad payload type")
        self._dirty = True