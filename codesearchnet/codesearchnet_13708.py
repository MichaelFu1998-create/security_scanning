def fix_in_stanza(self, stanza):
        """Fix an incoming stanza.

        Ona server replace the sender address with authorized client JID."""
        StreamBase.fix_in_stanza(self, stanza)
        if not self.initiator:
            if stanza.from_jid != self.peer:
                stanza.set_from(self.peer)