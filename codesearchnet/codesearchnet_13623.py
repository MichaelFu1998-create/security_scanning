def send_element(self, element):
        """
        Send an element via the transport.
        """
        with self.lock:
            if self._eof or self._socket is None or not self._serializer:
                logger.debug("Dropping element: {0}".format(
                                                element_to_unicode(element)))
                return
            data = self._serializer.emit_stanza(element)
            self._write(data.encode("utf-8"))