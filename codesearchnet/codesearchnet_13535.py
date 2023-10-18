def add_payload(self, payload):
        """Add new the stanza payload.

        Marks the stanza dirty.

        :Parameters:
            - `payload`: XML element or stanza payload object to add
        :Types:
            - `payload`: :etree:`ElementTree.Element` or `StanzaPayload`
        """
        if self._payload is None:
            self.decode_payload()
        if isinstance(payload, ElementClass):
            self._payload.append(XMLPayload(payload))
        elif isinstance(payload, StanzaPayload):
            self._payload.append(payload)
        else:
            raise TypeError("Bad payload type")
        self._dirty = True