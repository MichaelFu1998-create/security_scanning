def make_result_response(self):
        """Create result response for the a "get" or "set" iq stanza.

        :return: new `Iq` object with the same "id" as self, "from" and "to"
            attributes replaced and type="result".
        :returntype: `Iq`"""

        if self.stanza_type not in ("set", "get"):
            raise ValueError("Results may only be generated for"
                                                        " 'set' or 'get' iq")
        stanza = Iq(stanza_type = "result", from_jid = self.to_jid,
                        to_jid = self.from_jid, stanza_id = self.stanza_id)
        return stanza