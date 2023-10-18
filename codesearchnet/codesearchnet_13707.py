def fix_out_stanza(self, stanza):
        """Fix outgoing stanza.

        On a client clear the sender JID. On a server set the sender
        address to the own JID if the address is not set yet."""
        StreamBase.fix_out_stanza(self, stanza)
        if self.initiator:
            if stanza.from_jid:
                stanza.from_jid = None
        else:
            if not stanza.from_jid:
                stanza.from_jid = self.me