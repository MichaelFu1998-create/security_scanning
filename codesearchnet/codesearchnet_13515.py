def add_payload(self, payload):
        """Add new the stanza payload. Fails if there is already some
        payload element attached (<iq/> stanza can contain only one payload
        element)

        Marks the stanza dirty.

        :Parameters:
            - `payload`: XML element or stanza payload object to add
        :Types:
            - `payload`: :etree:`ElementTree.Element` or
              `interfaces.StanzaPayload`
        """
        if self._payload is None:
            self.decode_payload()
        if len(self._payload) >= 1:
            raise ValueError("Cannot add more payload to Iq stanza")
        return Stanza.add_payload(self, payload)