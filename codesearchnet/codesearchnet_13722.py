def _decode_subelements(self):
        """Decode the stanza subelements."""
        for child in self._element:
            if child.tag == self._show_tag:
                self._show = child.text
            elif child.tag == self._status_tag:
                self._status = child.text
            elif child.tag == self._priority_tag:
                try:
                    self._priority = int(child.text.strip())
                    if self._priority < -128 or self._priority > 127:
                        raise ValueError
                except ValueError:
                    raise BadRequestProtocolError(
                                            "Presence priority not an integer")