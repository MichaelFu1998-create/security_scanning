def copy(self):
        """Create a deep copy of the stanza.

        :returntype: `Stanza`"""
        result = Stanza(self.element_name, self.from_jid, self.to_jid,
                        self.stanza_type, self.stanza_id, self.error,
                        self._return_path())
        if self._payload is None:
            self.decode_payload()
        for payload in self._payload:
            result.add_payload(payload.copy())
        return result