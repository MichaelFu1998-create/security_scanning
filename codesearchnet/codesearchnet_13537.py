def get_payload(self, payload_class, payload_key = None,
                                                        specialize = False):
        """Get the first payload item matching the given class
        and optional key.

        Payloads may be addressed using a specific payload class or
        via the generic `XMLPayload` element, though the `XMLPayload`
        representation is available only as long as the element is not
        requested by a more specific type.

        :Parameters:
            - `payload_class`: requested payload class, a subclass of
              `StanzaPayload`. If `None` get the first payload in whatever
              class is available.
            - `payload_key`: optional key for additional match. When used
              with `payload_class` = `XMLPayload` this selects the element to
              match
            - `specialize`: If `True`, and `payload_class` is `None` then
              return object of a specialized `StanzaPayload` subclass whenever
              possible
        :Types:
            - `payload_class`: `StanzaPayload`
            - `specialize`: `bool`

        :Return: payload element found or `None`
        :Returntype: `StanzaPayload`
        """
        if self._payload is None:
            self.decode_payload()
        if payload_class is None:
            if self._payload:
                payload = self._payload[0]
                if specialize and isinstance(payload, XMLPayload):
                    klass = payload_class_for_element_name(
                                                        payload.element.tag)
                    if klass is not XMLPayload:
                        payload = klass.from_xml(payload.element)
                        self._payload[0] = payload
                return payload
            else:
                return None
        # pylint: disable=W0212
        elements = payload_class._pyxmpp_payload_element_name
        for i, payload in enumerate(self._payload):
            if isinstance(payload, XMLPayload):
                if payload_class is not XMLPayload:
                    if payload.xml_element_name not in elements:
                        continue
                    payload = payload_class.from_xml(payload.element)
            elif not isinstance(payload, payload_class):
                continue
            if payload_key is not None and payload_key != payload.handler_key():
                continue
            self._payload[i] = payload
            return payload
        return None