def __error(self,stanza):
        """Handle disco error response.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `pyxmpp.stanza.Stanza`"""
        try:
            self.error(stanza.get_error())
        except ProtocolError:
            from ..error import StanzaErrorNode
            self.error(StanzaErrorNode("undefined-condition"))