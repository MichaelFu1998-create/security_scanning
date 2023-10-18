def _send_stream_start(self, stream_id = None, stream_to = None):
        """Send stream start tag."""
        if self._output_state in ("open", "closed"):
            raise StreamError("Stream start already sent")
        if not self.language:
            self.language = self.settings["language"]
        if stream_to:
            stream_to = unicode(stream_to)
        elif self.peer and self.initiator:
            stream_to = unicode(self.peer)
        stream_from = None
        if self.me and (self.tls_established or not self.initiator):
            stream_from = unicode(self.me)
        if stream_id:
            self.stream_id = stream_id
        else:
            self.stream_id = None
        self.transport.send_stream_head(self.stanza_namespace,
                                        stream_from, stream_to,
                                    self.stream_id, language = self.language)
        self._output_state = "open"