def _decode_attributes(self):
        """Decode attributes of the stanza XML element
        and put them into the stanza properties."""
        try:
            from_jid = self._element.get('from')
            if from_jid:
                self._from_jid = JID(from_jid)
            to_jid = self._element.get('to')
            if to_jid:
                self._to_jid = JID(to_jid)
        except ValueError:
            raise JIDMalformedProtocolError
        self._stanza_type = self._element.get('type')
        self._stanza_id = self._element.get('id')
        lang = self._element.get(XML_LANG_QNAME)
        if lang:
            self._language = lang