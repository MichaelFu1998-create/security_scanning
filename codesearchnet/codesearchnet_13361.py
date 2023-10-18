def _decode_subelements(self):
        """Decode the stanza subelements."""
        for child in self._element:
            if child.tag == self._subject_tag:
                self._subject = child.text
            elif child.tag == self._body_tag:
                self._body = child.text
            elif child.tag == self._thread_tag:
                self._thread = child.text