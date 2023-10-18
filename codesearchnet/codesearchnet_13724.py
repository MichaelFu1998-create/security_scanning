def copy(self):
        """Create a deep copy of the stanza.

        :returntype: `Presence`"""
        result = Presence(None, self.from_jid, self.to_jid,
                        self.stanza_type, self.stanza_id, self.error,
                        self._return_path(),
                        self._show, self._status, self._priority)
        if self._payload is None:
            self.decode_payload()
        for payload in self._payload:
            result.add_payload(payload.copy())
        return result