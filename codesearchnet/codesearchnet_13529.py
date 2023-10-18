def _decode_error(self):
        """Decode error element of the stanza."""
        error_qname = self._ns_prefix + "error"
        for child in self._element:
            if child.tag == error_qname:
                self._error = StanzaErrorElement(child)
                return
        raise BadRequestProtocolError("Error element missing in"
                                                            " an error stanza")