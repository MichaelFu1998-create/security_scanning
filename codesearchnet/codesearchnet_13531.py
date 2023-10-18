def as_xml(self):
        """Return the XML stanza representation.

        Always return an independent copy of the stanza XML representation,
        which can be freely modified without affecting the stanza.

        :returntype: :etree:`ElementTree.Element`"""
        attrs = {}
        if self._from_jid:
            attrs['from'] = unicode(self._from_jid)
        if self._to_jid:
            attrs['to'] = unicode(self._to_jid)
        if self._stanza_type:
            attrs['type'] = self._stanza_type
        if self._stanza_id:
            attrs['id'] = self._stanza_id
        if self._language:
            attrs[XML_LANG_QNAME] = self._language
        element = ElementTree.Element(self._element_qname, attrs)
        if self._payload is None:
            self.decode_payload()
        for payload in self._payload:
            element.append(payload.as_xml())
        if self._error:
            element.append(self._error.as_xml(
                                        stanza_namespace = self._namespace))
        return element