def make_accept_response(self):
        """Create "accept" response for the "subscribe" / "subscribed" /
        "unsubscribe" / "unsubscribed" presence stanza.

        :return: new stanza.
        :returntype: `Presence`
        """
        if self.stanza_type not in ("subscribe", "subscribed",
                                                "unsubscribe", "unsubscribed"):
            raise ValueError("Results may only be generated for 'subscribe',"
                "'subscribed','unsubscribe' or 'unsubscribed' presence")
        stanza = Presence(stanza_type = ACCEPT_RESPONSES[self.stanza_type],
                            from_jid = self.to_jid, to_jid = self.from_jid,
                                                    stanza_id = self.stanza_id)
        return stanza