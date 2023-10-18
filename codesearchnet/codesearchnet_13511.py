def __response(self,stanza):
        """Handle successful disco response.

        :Parameters:
            - `stanza`: the stanza received.
        :Types:
            - `stanza`: `pyxmpp.stanza.Stanza`"""
        try:
            d=self.disco_class(stanza.get_query())
            self.got_it(d)
        except ValueError,e:
            self.error(e)