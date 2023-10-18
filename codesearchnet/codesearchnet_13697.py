def _send(self, stanza):
        """Same as `send` but assume `lock` is acquired."""
        self.fix_out_stanza(stanza)
        element = stanza.as_xml()
        self._write_element(element)