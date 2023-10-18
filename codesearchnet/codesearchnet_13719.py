def handle_message(self, stanza):
        """Echo every non-error ``<message/>`` stanza.
        
        Add "Re: " to subject, if any.
        """
        if stanza.subject:
            subject = u"Re: " + stanza.subject
        else:
            subject = None
        msg = Message(stanza_type = stanza.stanza_type,
                        from_jid = stanza.to_jid, to_jid = stanza.from_jid,
                        subject = subject, body = stanza.body,
                        thread = stanza.thread)
        return msg