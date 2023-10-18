def copy(self):
        """Create a deep copy of the stanza.

        :returntype: `Message`"""
        result = Message(None, self.from_jid, self.to_jid,
                        self.stanza_type, self.stanza_id, self.error,
                        self._return_path(), self._subject, self._body,
                                                            self._thread)
        for payload in self._payload:
            result.add_payload(payload.copy())
        return result