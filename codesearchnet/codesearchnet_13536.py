def get_all_payload(self, specialize = False):
        """Return list of stanza payload objects.

        :Parameters:
            - `specialize`: If `True`, then return objects of specialized
              `StanzaPayload` classes whenever possible, otherwise the
              representation already available will be used (often
              `XMLPayload`)

        :Returntype: `list` of `StanzaPayload`
        """
        if self._payload is None:
            self.decode_payload(specialize)
        elif specialize:
            for i, payload in enumerate(self._payload):
                if isinstance(payload, XMLPayload):
                    klass = payload_class_for_element_name(
                                                        payload.element.tag)
                    if klass is not XMLPayload:
                        payload = klass.from_xml(payload.element)
                        self._payload[i] = payload
        return list(self._payload)