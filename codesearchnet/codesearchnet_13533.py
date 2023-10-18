def decode_payload(self, specialize = False):
        """Decode payload from the element passed to the stanza constructor.

        Iterates over stanza children and creates StanzaPayload objects for
        them. Called automatically by `get_payload()` and other methods that
        access the payload.

        For the `Stanza` class stanza namespace child elements will also be
        included as the payload. For subclasses these are no considered
        payload."""
        if self._payload is not None:
            # already decoded
            return
        if self._element is None:
            raise ValueError("This stanza has no element to decode""")
        payload = []
        if specialize:
            factory = payload_factory
        else:
            factory = XMLPayload
        for child in self._element:
            if self.__class__ is not Stanza:
                if child.tag.startswith(self._ns_prefix):
                    continue
            payload.append(factory(child))
        self._payload = payload